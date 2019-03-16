###############################################################################
# Participant model
# by Dillon Bowen
# last modified 03/16/2019
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

'''
TODO
CLEAR EMBEDDED DATA FROM PARTICIPANT ON BACK FROM BRANCH
workerId in metadata
distinguish private from public functions
'''

###############################################################################
# Login participant
###############################################################################

@login.user_loader
def load_user(id):
    return Participant.query.get(int(id))



'''
Data:
    page_queue: queue of pages to be displayed
    questions: questions assigned to participant
    variables: variables the participant contributes to dataframe
    
    data: dictionary of data participant contributes to dataset
    g: participant-specific global dictionary
    head: index of current page in page queue
    num_rows: number of rows participant contributes to dataframe
    metadata: list of participant metadata variables
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
        backref='_part_head',
        uselist=False,
        foreign_keys='Branch._part_head_id')
    
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
    _head = db.Column(db.Integer, default=0)
    _num_rows = db.Column(db.Integer, default=0)
    _metadata = db.Column(db.PickleType, 
        default=['id','ipv4','start_time','end_time','completed'])
    
    # Initialize participant
    # login user
    # record metadata
    # create an initial checkpoint (root)
    # advance to first page
    def __init__(self, ipv4, start): 
        db.session.add(self)
        db.session.commit()
        login_user(self)
        
        self.record_metadata(ipv4)
        
        root = Branch(next=start)
        self._insert_children([root])
        self._current_branch = root
        self._forward()
            
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
    def record_metadata(self, ipv4):
        Variable(self, 'id', True, self.id)
        Variable(self, 'ipv4', True, ipv4)
        Variable(self, 'start_time', True, datetime.utcnow())
        Variable(self, 'end_time', True, datetime.utcnow())
        Variable(self, 'completed', True, 0)
        
    # Update metadata (end time and completed indicator)
    def update_metadata(self, completed_indicator=False):
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
    def get_data(self):
        return self._data
            
    # Store participant data
    # update current data
    # pad variables to even length and store
    def store_data(self, completed_indicator=False): 
        self.clear_data()
        [self.process_question(q) 
			for q in self._questions if q._var]
        self.update_metadata(completed_indicator)
        
        [var.pad(self._num_rows) for var in self._variables]
        self._data = {var.name:var.data for var in self._variables}
        db.session.commit()
        
    # Clear participant data
    def clear_data(self):
        [db.session.delete(v) 
            for v in self._variables.all() if v.name not in self._metadata]
        [v.set_num_rows(0) for v in self._variables]
        self._num_rows = 0
        
    # Process question data
    # get variables associated with question data
    # pad variables to even length
    # write question data to these variables
    def process_question(self, q):
        qdata = q._output_data()
        
        vars = [self.get_var(name, q._all_rows) 
            for name in qdata.keys()]
        
        max_rows = max(v.num_rows for v in vars)
        [var.pad(max_rows) for var in vars]

        vars.sort(key=lambda x: x.name)
        [var.add_data(qdata[name]) for (name,var) in zip(sorted(qdata),vars)]
        
    # Get variable associated with variable name
    # create new variable if needed
    # all_rows: indicates the variable should contain the same data in all rows
    def get_var(self, name, all_rows):
        var = [v for v in self._variables if v.name == name]
        if not var:
            return Variable(self, name, all_rows)
        return var[0]
        
        
        
    ###########################################################################
    # Navigation
    ###########################################################################
        
    # Return the current page
    def _get_current_page(self):
        return self._current_branch._current_page
        
    # Advance to the next page
    def _forward(self):
        current_page = self._get_current_page()
    
        if current_page is None:
            return self._terminate_branch()
            
        current_page.participant()

        if current_page._next_function is not None:
            return self._insert_branch(current_page)
            
        self._current_branch._forward()
        self._continue_forward_to_page()
        
        new_current_page = self._get_current_page()
        if new_current_page._terminal:
            new_current_page.participant()
        
    # Terminate a branch when the end of the page queue is reached
    def _terminate_branch(self):
        if (self._current_branch._next_function is not None 
            and self._current_branch._next_branch is None):
            return self._insert_branch(self._current_branch)
        self._decrement_head()
        self._current_branch._forward()
        self._continue_forward_to_page()

    # Inserts a branch created by the origin
    # origin may be a page or branch
    def _insert_branch(self, origin):
        new_branch = origin._grow_branch()
        new_branch.participant()
        self._insert_children([new_branch], self._current_branch._index+1)
        self._advance_head()
        self._continue_forward_to_page()
        
    # Continue advancing forward until participant reaches a page
    def _continue_forward_to_page(self):
        if self._get_current_page() is not None:
            return
        self._forward()
        
    # Advance head pointer to next branch in stack
    def _advance_head(self):
        new_head_index = self._current_branch._index + 1
        self._current_branch = self._branch_stack[new_head_index]
            
    # Decrements head pointer to previous branch in stack
    def _decrement_head(self):
        new_head_index = self._current_branch._index - 1
        self._current_branch = self._branch_stack[new_head_index]    
        
    # Return to the previous page
    def _back(self):
        pass