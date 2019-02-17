###############################################################################
# Participant model
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

from hemlock import db
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable
from flask import request
import pandas as pd
from datetime import datetime

'''
TODO
security
format
CLEAR EMBEDDED DATA FROM PARTICIPANT ON BACK FROM BRANCH
'''

'''
Data:
page_queue: queue of pages to be displayed
questions: question assigned to participant
variables: variables the participant contributes to dataframe
num_rows: number of rows participant contributes to dataframe
'''
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.Integer, default=0)
    data = db.Column(db.PickleType)
    
    page_queue = db.relationship('Page', backref='_part', lazy='dynamic',
        order_by='Page._queue_order')
    questions = db.relationship('Question', backref='_part', lazy='dynamic',
        order_by='Question.id')
    variables = db.relationship('Variable', backref='part', lazy='dynamic')
    num_rows = db.Column(db.Integer, default=0)
    endtime = db.Column(db.DateTime, default=datetime.utcnow())
    __metadata = db.Column(db.PickleType, 
        default=['id','ipv4','start_time','end_time','completed']) # HAVE SEPARATE VARLIST FOR METADATA
    
    def __init__(self, ipv4, start): 
        db.session.add(self)
        db.session.commit()
        
        self.record_metadata(ipv4)
        
        root = Page(next=start)
        root._initialize()
        root._part_id = self.id
        root._queue_order = 0
        self.print_queue()
        
        # continue advancing past checkpoints until you hit a regular page
        while self.get_page()._checkpoint:
            self.process_checkpoint()
                
    def print_queue(self):
        print('queue')
        for p in self.page_queue:
            star = '***' if p == self.get_page() else ''
            print(p, p._checkpoint, p._queue_order, star)
                
    # Record participant metadata
    def record_metadata(self, ipv4):
        Variable(self, 'id', True, self.id)
        Variable(self, 'ipv4', True, ipv4)
        Variable(self, 'start_time', True, datetime.utcnow())
        Variable(self, 'end_time', True, datetime.utcnow())
        Variable(self, 'completed', True, 0)
        self.store_data()
        
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
        self.get_page()._set_direction('forward')
        
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
        self.get_page()._set_direction('back')
        
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
    def store_data(self, completed_indicator=False):
        # clear data from previous store
        self.clear_data()

        # process data from questions
        [self.process_question(q) 
			for q in self.questions if q._var]
            
        # update end time and completed status
        self.update_metadata(completed_indicator)
            
        # pad variables to even length and store in data dictionary
        [var.pad(self.num_rows) for var in self.variables]
        self.data = {var.name:var.data for var in self.variables}
        
        db.session.commit()
        
    # Get variable associated with variable name
    # create new variable if needed
    def get_var(self, name, all_rows):
        var = [v for v in self.variables if v.name == name]
        if not var:
            return Variable(self, name, all_rows)
        return var[0]
        
    # Process question data
    def process_question(self, q):
        qdata = q._output_data()
        
        # get variables associated with question data
        vars = [self.get_var(name, q._all_rows) 
            for name in qdata.keys()]
        
        # pad variables
        max_rows = max(v.num_rows for v in vars)
        [var.pad(max_rows) for var in vars]
        
        # write data to variables
        vars.sort(key=lambda x: x.name)
        [var.add_data(qdata[name]) for (name,var) in zip(sorted(qdata),vars)]
        
    # Update metadata (end time and completed indicator)
    def update_metadata(self, completed_indicator=False):
        metadata = [v for v in self.variables 
            if v.name in ['end_time','completed']]
        metadata.sort(key=lambda x: x.name)
        completed, endtime = metadata
        endtime.data = [self.endtime]
        completed.data = [int(completed_indicator)]
        
        
