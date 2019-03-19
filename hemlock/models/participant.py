###############################################################################
# Participant model
# by Dillon Bowen
# last modified 03/19/2019
###############################################################################

from hemlock.factory import db, login
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable
from hemlock.models.private.base import Base
from flask import request
from flask_login import UserMixin, login_user
from datetime import datetime
from copy import deepcopy



###############################################################################
# Login participant
###############################################################################

@login.user_loader
def load_user(id):
    return Participant.query.get(int(id))



'''
Relationships:
    branch_stack: stack of branches to be displayed
    current_branch: head of the branch stack
    pages: set of pages belonging to the participant
    questions: set of questions belonging to the participant
    variables: set of variables participant contributes to dataset
    
Columns:
    data: dictionary of data participant contributes to dataset
    g: global dictionary, accessible from navigation functions
    num_rows: number of rows participant contributes to dataset
    metadata: participant metadata (e.g. start and end time)
'''
class Participant(db.Model, UserMixin, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _branch_stack = db.relationship(
        'Branch',
        backref='_part',
        lazy='dynamic',
        order_by='Branch._index',
        foreign_keys='Branch._part_id')
        
    _current_branch = db.relationship(
        'Branch',
        uselist=False,
        foreign_keys='Branch._part_head_id')
        
    _pages = db.relationship(
        'Page',
        backref='_part',
        lazy='dynamic')
    
    _questions = db.relationship(
        'Question', 
        backref='_part', 
        lazy='dynamic',
        order_by='Question.id')
        
    _variables = db.relationship(
        'Variable', 
        backref='part', 
        lazy='dynamic')
    
    _data = db.Column(db.PickleType)
    _g = db.Column(db.PickleType, default={})
    _num_rows = db.Column(db.Integer, default=0)
    _metadata = db.Column(db.PickleType, 
        default=['id','ipv4','start_time','end_time','completed'])
    
    
    
    # Initialize participant
    # login user
    # record metadata
    # initialize branch stack with root branch
    def __init__(self, ipv4, start): 
        db.session.add(self)
        db.session.commit()
        login_user(self)
        
        self._record_metadata(ipv4)
        
        root = Branch(next=start)
        root.participant()
        self._current_branch = root
        self._forward_recurse()
            
        db.session.commit()
        
        
        
    ###########################################################################
    # Global dictionary
    ###########################################################################
    
    # Modify participant's global dictionary
    # modification is a dictionary
    def modg(self, modification):
        temp = deepcopy(self._g)
        for key,value in modification.items():
            temp[key]=value
        self._g = deepcopy(temp)
    
    # Inspect participant's global dictionary
    # to_get may be list, dictionary, or key
    # nested lists and dictionaries are allowed
    def g(self, to_get):
        if type(to_get) is list:
            return [self.g(x) for x in to_get]
        if type(to_get) is dict:
            return {key:self.g(val) for (key,val) in to_get.items()}
        if to_get in self._g.keys():
            return self._g[to_get]


    
    ###########################################################################
    # Metadata
    ###########################################################################
    
    # Record participant metadata
    def _record_metadata(self, ipv4):
        Variable(self, 'id', True, self.id)
        Variable(self, 'ipv4', True, ipv4)
        Variable(self, 'start_time', True, datetime.utcnow())
        Variable(self, 'end_time', True, datetime.utcnow())
        Variable(self, 'completed', True, 0)
        
    # Update metadata (end time and completed indicator)
    def _update_metadata(self, completed_indicator=False):
        metadata = [v for v in self._variables 
            if v.name in ['end_time','completed']]
        metadata.sort(key=lambda x: x.name)
        completed, endtime = metadata
        endtime.data = [datetime.utcnow()]
        completed.data = [int(completed_indicator)]
        
        
        
    ###########################################################################
    # Data storage
    ###########################################################################
    
    # Return a dictionary of participant data
    def _get_data(self):
        return self._data
            
    # Store participant data
    # update current data
    # pad variables to even length and store
    def _store_data(self, completed_indicator=False): 
        self._clear_data()
        [self._process_question(q) 
			for q in self._questions if q._var]
        self._update_metadata(completed_indicator)
        
        [var.pad(self._num_rows) for var in self._variables]
        self._data = {var.name:var.data for var in self._variables}
        db.session.commit()
        
    # Clear participant data
    def _clear_data(self):
        [db.session.delete(v) 
            for v in self._variables.all() if v.name not in self._metadata]
        [v.set_num_rows(0) for v in self._variables]
        self._num_rows = 0
        
    # Process question data
    # get variables associated with question data
    # pad variables to even length
    # write question data to these variables
    def _process_question(self, q):
        qdata = q._output_data()
        
        vars = [self._get_var(name, q._all_rows) 
            for name in qdata.keys()]
        
        max_rows = max(v.num_rows for v in vars)
        [var.pad(max_rows) for var in vars]

        vars.sort(key=lambda x: x.name)
        [var.add_data(qdata[name]) for (name,var) in zip(sorted(qdata),vars)]
        
    # Get variable associated with variable name
    # create new variable if needed
    # all_rows: indicates the variable should contain the same data in all rows
    def _get_var(self, name, all_rows):
        var = [v for v in self._variables if v.name == name]
        if not var:
            return Variable(self, name, all_rows)
        return var[0]
        
        
        
    ###########################################################################
    # Forward navigation
    ###########################################################################
    
    # Advance forward to next page
    # assign new current branch to participant if terminal
    def _forward(self):
        current_page = self._get_current_page()
        current_page.participant()
        
        if current_page._eligible_to_insert_next():
            self._insert_branch(current_page)
        else:
            self._current_branch._forward()
            self._forward_recurse()
        
        new_current_page = self._get_current_page()
        if new_current_page._terminal:
            new_current_page.participant()
    
    # Inserts a branch created by the origin
    # origin may be a page or branch
    def _insert_branch(self, origin):
        new_branch = origin._grow_branch()
        new_branch.participant(index=self._current_branch._index+1)
        self._increment_head()
        self._forward_recurse()
        
    # Recursive forward function
    # move through survey pages until it finds the next page
    def _forward_recurse(self):
        current_page = self._get_current_page()
        
        if current_page is None:
            if self._current_branch._eligible_to_insert_next():
                self._insert_branch(self._current_branch)
            else:
                self._decrement_head()
                self._current_branch._forward()
            return self._forward_recurse()
        
        
        
    ###########################################################################
    # Backward navigation
    ###########################################################################
            
    # Return to the previous page
    def _back(self):
        current_page = self._get_current_page()
        current_page.remove_participant()
        
        if current_page == self._current_branch._page_queue.first():
            return self._remove_branch()
            
        self._current_branch._back()
        self._back_recurse()
        
    # Remove the current branch from stack
    def _remove_branch(self):
        current_head_index = self._current_branch._index
        self._current_branch.remove_participant()
        self._decrement_head(current_head_index)
        self._back_recurse()
        
    # Recursive back function
    # move through survey pages until it finds the previous page
    def _back_recurse(self):
        current_page = self._get_current_page()
        
        if current_page is None:
            if self._current_branch._next_branch in self._branch_stack.all():
                self._increment_head()
            elif self._current_branch._page_queue.all():
                self._current_branch._back()
            else:
                return self._remove_branch()
            return self._back_recurse()
            
        if current_page._next_branch not in self._branch_stack.all():
            return
        self._increment_head()
        self._back_recurse()
        
        
    
    ###########################################################################
    # General navigation and debugging
    ###########################################################################
    
    # Return the current page
    def _get_current_page(self):
        return self._current_branch._current_page

    # Advance head pointer to next branch in stack
    def _increment_head(self):
        new_head_index = self._current_branch._index + 1
        self._current_branch = self._branch_stack[new_head_index]
            
    # Decrements head pointer to previous branch in stack
    def _decrement_head(self, head_index=None):
        if head_index is None:
            head_index = self._current_branch._index
        new_head_index = head_index - 1
        self._current_branch = self._branch_stack[new_head_index] 
        
    # Print branch stack
    def _print_branch_stack(self):
        for b in self._branch_stack.all():
            if b == self._current_branch:
                print(b, '***')
            else:
                print(b)
            b._print_page_queue()