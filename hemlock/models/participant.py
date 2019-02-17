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
from sqlalchemy.ext.orderinglist import ordering_list
import pandas as pd
from datetime import datetime

'''
TODO
have 'checkpoint' instead of those ugly tuples
constant time find next checkpoint in back

Give checkpoint the get_next responsibilities
including randomizing pages and assigning embedded data to participant

Things you can't do without checkpoint:
    randomize pages within branch
    unassign embedded data when going back over a branch
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
        order_by='Page._queue_order', collection_class=ordering_list('_queue_order'))
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
        self.page_queue = [root]
        '''        
        # root = Branch(next=start)
        # self.queue = [self.next_tuple(root)]
        '''
        
        # continue advancing past checkpoints until you hit a regular page
        while self.get_page()._checkpoint:
            self.process_checkpoint()
        '''
        while type(self.queue[self.head]) != int:
            self.process_next()
        '''
            
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
     
    '''
    # Get the next tuple (function, args, branch_id, page_id)
    # orig: from which the next function originates (Branch or Page)
    def next_tuple(self, orig):
        return [orig._next_function, orig._next_args, orig.id, orig.__class__]
    '''
        
    # Inserts a list into the queue split at head
    def insert_to_queue(self, insert):
        if insert is None:
            return
        self.page_queue = (
            self.page_queue[:self.head]
            +insert
            +self.page_queue[self.head:])
        
    # Go forward to next page
    def forward(self):
        # get current head and advance head pointer
        head = self.get_page()
        self.head += 1
        
        # create a checkpoint for the current page's branch
        if head._next_function is not None:
            checkpoint = Page()
            self.insert_to_queue([checkpoint.__(head)])
            
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
        next_checkpoint = Page()
        next_checkpoint._initialize(next_branch)
        to_insert = next_branch._page_queue.all() + [next_checkpoint]
        
        # insert next branch's page queue and next checkpoint to queue
        self.insert_to_queue(to_insert)
        '''
        # extract next function, args, and origin id and table from next tuple
        function, args, origin_id, table = self.queue[self.head]
        
        if function is None:
            self.head += 1
            return
            
        # get next branch and assign embedded data to participant
        if args is None:
            next = function()
        else:
            next = function(args)
        [e._assign_participant(self.id) for e in next._embedded]
            
        # update origin next branch id
        if table is not None:
            table.query.get(origin_id)._id_next = next.id
        
        # insert next branch pages and next tuple into queue
        insert = next._get_page_ids()+[self.next_tuple(next)]
        self.head += 1
        self.insert_list(insert)
        '''
        
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
                self.page_queue = (
                    self.page_queue[:start] + self.page_queue[end+1:])
                    
            self.head -= 1
        
        '''
        while type(self.queue[self.head]) != int:
            function, args, id, table = self.queue[self.head]
            if function is not None:
                # find next navigator
                # FIND A WAY TO DO THIS IN CONSTANT TIME
                temp = self.head+1
                while type(self.queue[temp]) == int:
                    temp += 1
                    
                # remove elements in between
                # NOTE: CHECKPOINT IS CREATED AFTER PAGE WITH PAGE BRANCH IS RENDERED. THEREFORE NEED TO DELETE THIS CHECKPOINT WHEN GOING BACK. HENCE, WHEN TABLE==PAGE, START INDEX IS 1 BEFORE START INDEX WHEN TABLE==BRANCH
                # REMOVE BRANCH EMBEDDED DATA FROM PARTICIPANT HERE!!!
                # this is another checkpoint responsibility
                if table == Page:
                    index = self.head
                elif table == Branch:
                    index = self.head+1
                self.queue = self.queue[:index] + self.queue[temp+1:]
                
            # decrement head
            self.head -= 1
        '''

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
    def update_metadata(self, completed_indicator):
        metadata = [v for v in self.variables 
            if v.name in ['end_time','completed']]
        metadata.sort(key=lambda x: x.name)
        completed, endtime = metadata
        endtime.data = [self.endtime]
        completed.data = [int(completed_indicator)]
        
        
