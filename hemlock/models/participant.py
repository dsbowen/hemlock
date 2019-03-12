###############################################################################
# Participant model
# by Dillon Bowen
# last modified 03/12/2019
###############################################################################

from hemlock.factory import db, login
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable
from flask import request
from flask_login import UserMixin, login_user
import pandas as pd
from datetime import datetime
from copy import deepcopy

'''
TODO
CLEAR EMBEDDED DATA FROM PARTICIPANT ON BACK FROM BRANCH
'''

@login.user_loader
def load_user(id):
    return Participant.query.get(int(id))

'''
Data:
    data: dictionary of data participant contributes to dataset
    end_time: last recorded activity on survey
    g: participant-specific global dictionary
    head: index of current page in page queue
    num_rows: number of rows participant contributes to dataframe
    
    page_queue: queue of pages to be displayed
    questions: questions assigned to participant
    variables: variables the participant contributes to dataframe
    
    __metadata: list of participant metadata variables
'''
class Participant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.PickleType)
    endtime = db.Column(db.DateTime, default=datetime.utcnow())
    _g = db.Column(db.PickleType, default={})
    head = db.Column(db.Integer, default=0)
    num_rows = db.Column(db.Integer, default=0)
    
    page_queue = db.relationship('Page', backref='_part', lazy='dynamic',
        order_by='Page._queue_order')
    questions = db.relationship('Question', backref='_part', lazy='dynamic',
        order_by='Question.id')
    variables = db.relationship('Variable', backref='part', lazy='dynamic')
    
    __metadata = db.Column(db.PickleType, 
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
        root._initialize()
        root._part_id = self.id
        root._queue_order = 0

        while self.get_page()._checkpoint:
            self.process_checkpoint()
            
        db.session.commit()
        
        
        
    ###########################################################################
    # Global dictionary
    ###########################################################################
    
    # Inspect participant's global dictionary by keys
    # keys may be a list of keys, a dictionary of keys, or a single key
    def g(self, keys):
        # return a list if keys are stored in a list
        if type(keys) is list:
            to_return = []
            for key in keys:
                if key in self._g.keys():
                    to_return.append(self._g[key])
                else:
                    to_return.append(None)
            return to_return
            
        # return a dict if keys are stored in dict
        if type(keys) is dict:
            to_return = {}
            for key, value in keys.items():
                if value in self._g.keys():
                    to_return[key] = self._g[value]
                else:
                    to_return[key] = None
            return to_return
            
        # return a value if keys is a single value
        if keys in self._g.keys():
            return self._g[keys]
        
    # Modify participant's global dictionary
    # modification is a dictionary
    def modg(self, modification):
        temp = deepcopy(self._g)
        for key,value in modification.items():
            temp[key]=value
        self._g = deepcopy(temp)


    
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
        metadata = [v for v in self.variables 
            if v.name in ['end_time','completed']]
        metadata.sort(key=lambda x: x.name)
        completed, endtime = metadata
        endtime.data = [self.endtime]
        completed.data = [int(completed_indicator)]
        
        
        
    ###########################################################################
    # Data storage
    ###########################################################################
    
    # Return a dictionary of participant data
    def get_data(self):
        return self.data
            
    # Clear participant data
    def clear_data(self):
        [db.session.delete(v) 
            for v in self.variables.all() if v.name not in self.__metadata]
        [v.set_num_rows(0) for v in self.variables]
        self.num_rows = 0
            
    # Store participant data
    # update current data
    # pad variables to even length and store
    def store_data(self, completed_indicator=False): 
        self.clear_data()
        [self.process_question(q) 
			for q in self.questions if q._var]
        self.update_metadata(completed_indicator)
        
        [var.pad(self.num_rows) for var in self.variables]
        self.data = {var.name:var.data for var in self.variables}
        db.session.commit()
        
    # Get variable associated with variable name
    # create new variable if needed
    # all_rows: indicates the variable should contain the same data in all rows
    def get_var(self, name, all_rows):
        var = [v for v in self.variables if v.name == name]
        if not var:
            return Variable(self, name, all_rows)
        return var[0]
        
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
        
        
        
    ###########################################################################
    # Page navigation
    ###########################################################################  

    # Return current page
    def get_page(self):
        return self.page_queue[self.head]
        
    # Insert a list into the queue split at head
    def insert_to_queue(self, insert):
        if insert is None:
            return
            
        # push pages after head down in the queue
        [p._modify_queue_order(len(insert)) for p in self.page_queue[self.head:]]
        
        # insert new pages
        [insert[i]._insert_to_queue(self.id, self.head+i) for i in range(len(insert))]
        
    # Go forward to next page
    def forward(self):
        # get current head and advance head pointer
        head = self.get_page()
        self.head += 1
        
        # create a checkpoint for the current page's branch
        if head._next_function is not None:
            checkpoint = Page()
            self.insert_to_queue([checkpoint._initialize(head)])
            
        # continue processing checkpoints until you hit a regular page
        while self.get_page()._checkpoint:
            self.process_checkpoint()
            
        # set page direction to forward
        self.get_page()._set_direction_to('forward')
        
    # Process checkpoint
    def process_checkpoint(self):
        # get the current checkpoint and increment head
        checkpoint = self.get_page()
        self.head += 1
        
        # create the next branch and checkpoint
        next_branch = checkpoint._get_next()
        if next_branch is None:
            return
        next_checkpoint = Page()
        next_checkpoint._initialize(next_branch)
        to_insert = next_branch._page_queue.all() + [next_checkpoint]

        # insert next branch's page queue and next checkpoint to queue
        self.insert_to_queue(to_insert)
        
    # Go backward to previous page
    def back(self):    
        # decrement head
        self.head -= 1
        
        # continue backward until you hit a regular page
        while self.get_page()._checkpoint:
            checkpoint = self.get_page()
            if checkpoint._next_function is not None:
                start = checkpoint._queue_order
                if checkpoint._origin_table == Branch:
                    start += 1
                end = checkpoint._get_branch_end()
                
                # remove branch from queue
                [p._remove_from_queue() for p in self.page_queue[start:end+1]]
                
                # push back pages after branch
                [p._modify_queue_order(start-end-1) for p in self.page_queue[start:]]
                    
            self.head -= 1

        # set direction to back
        self.get_page()._set_direction_to('back')