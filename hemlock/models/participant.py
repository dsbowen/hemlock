###############################################################################
# Participant model
# by Dillon Bowen
# last modified 03/15/2019
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
    
    _page_queue = db.relationship('Page', backref='_part', lazy='dynamic',
        order_by='Page._queue_order')
    _questions = db.relationship('Question', backref='_part', lazy='dynamic',
        order_by='Question.id')
    _variables = db.relationship('Variable', backref='part', lazy='dynamic')
    
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
        
        root = Page(next=start)
        root._initialize_as_checkpoint()
        root._part_id = self.id
        root._queue_order = 0

        while self.get_page()._checkpoint:
            self.process_checkpoint()
            
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

    # Return current page
    def get_page(self):
        return self._page_queue[self._head]
        
    # Go forward to next page
    # get current head, assign to participant, and advance head pointer
    # create a checkpoint for the page's branch (if applicable)
    # process checkpoints until head points to a non-checkpoint page
    # set next page direction_to to forward
    # assign embedded data to participant and record responses on terminal page
    def forward(self):
        head = self.get_page()
        head.participant()
        self._head += 1
        
        if head._next_function is not None:
            checkpoint = Page()._initialize_as_checkpoint(head)
            self._insert_children([checkpoint], self._head)
            
        while self.get_page()._checkpoint:
            self.process_checkpoint()
            
        self.get_page()._set_direction_to('forward')
            
        if self.get_page()._terminal:
            self.get_page().participant()
            self.store_data(completed_indicator=True)
        
    # Process checkpoint
    # get current checkpoint and advance head pointer
    # create the next branch and assign embedded data to participant
    # set up corresponding checkpoint
    # insert the next branch's pages to page queue
    def process_checkpoint(self):
        checkpoint = self.get_page()
        self._head += 1

        next_branch = checkpoint._get_next()
        if next_branch is None:
            return
        next_branch.participant()
        
        next_checkpoint = Page()._initialize_as_checkpoint(next_branch)
        to_insert = next_branch._page_queue.all() + [next_checkpoint]

        self._insert_children(to_insert, self._head)
        
    # Go backward to previous page
    # remove head from participant and decrement head
    # go back across checkpoints until head points to a non-checkpoint page
    # set next page direction_to to back
    def back(self):
        self.get_page().remove_participant()
        self._head -= 1
        
        while self.get_page()._checkpoint:
            checkpoint = self.get_page()
            if checkpoint._next_function is not None:
                start, end = checkpoint._get_branch_endpoints()
                self._remove_children('_page_queue', start, end)
            self._head -= 1
        
        self.get_page()._set_direction_to('back')
        
    # Print the page queue
    # for debugging purposes
    def print_queue(self):
        print(self._head)
        for p in self._page_queue:
            di = str(p._queue_order)
            if p._checkpoint:
                di += 'c'
            if p == self.get_page():
                di += '***'
            print(p, di)