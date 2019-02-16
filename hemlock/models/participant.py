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
from sqlalchemy import and_
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
branch_stack: stack of branches
curr_page: current page
questions: question assigned to participant
variables: variables the participant contributes to dataframe
data: data dictionary contributed to dataframe
num_rows: number of rows participant contributes to dataframe
'''
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    queue = db.Column(db.PickleType)
    head = db.Column(db.Integer, default=0)
    
    questions = db.relationship('Question', backref='_part', lazy='dynamic')
    variables = db.relationship('Variable', backref='part', lazy='dynamic')
    data = db.Column(db.PickleType)
    num_rows = db.Column(db.Integer, default=0)
    
    # Add participant to database and commit on initialization
    # also initialize participant id and start time questions
    def __init__(self, ipv4, start): 
        db.session.add(self)
        db.session.commit()
        
        self.record_metadata(ipv4)
        
        root = Branch(next=start)
        self.queue = [self.next_tuple(root)]
        
        # continue advancing until you hit a page
        while type(self.queue[self.head]) != int:
            self.process_next()
            
    # Record participant metadata
    def record_metadata(self, ipv4):
        metadata = [
            Question(var='id', data=self.id),
            Question(var='ipv4', data=ipv4),
            Question(var='start_time', data=datetime.utcnow()),
            Question(var='end_time', data=datetime.utcnow()),
            Question(var='completed', data=0)
            ]
        [q.all_rows() for q in metadata]
        [q._assign_participant(self.id) for q in metadata]
        self.store_data()
        
    # Update the end time
    def endtime(self):
        endtime = Question.query.filter_by(_part_id=self.id,_var='end_time')
        endtime = endtime.first()
        endtime.data(datetime.utcnow())
        
    # Return current page
    def get_page(self):
        return Page.query.get(self.queue[self.head])
        
    # Get the next tuple (function, args, branch_id, page_id)
    # orig: from which the next function originates (Branch or Page)
    def next_tuple(self, orig):
        return [orig._next_function, orig._next_args, orig.id, orig.__class__]
        
    # Inserts a list into the queue split at head
    def insert_list(self, insert):
        self.queue = self.queue[:self.head]+insert+self.queue[self.head:]
        
    # Go forward to next page
    def forward(self):
        # get current head and advance head pointer
        head = self.get_page()
        self.head += 1
        
        # process page branch
        if head._next_function is not None:
            self.insert_list([self.next_tuple(head)])
            
        # continue advancing until you hit a page
        while type(self.queue[self.head]) != int:
            self.process_next()
            
        # set page direction to forward
        self.get_page()._set_direction('forward')
        
    # Process item on queue if it contains the next navigation function
    def process_next(self):
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
        
    # Go backward to previous page
    def back(self):    
        # decrement head
        self.head -= 1
        
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

        # set direction to back
        self.get_page()._set_direction('back')
            
    # Clear participant data
    def clear_data(self):
        [db.session.delete(v) for v in self.variables.all()]
        self.num_rows = 0
        self.data = {}
            
    # Store participant data
    # add end time variable
    # processes data from each question the participant answered
    # pads variables so they are all of equal length
    # clears branches, pages, and questions from database
    def store_data(self, completed_indicator=False):
        self.clear_data()
        
        completed = Question.query.filter_by(_part_id=self.id,_var='completed')
        completed = completed.first()
        completed.data(completed_indicator)
        
        # process data from questions
        [self.process_question(q) 
			for q in self.questions.order_by('_id_orig') if q._var]
            
        # pad variables to even length and store in data dictionary
        [var.pad(self.num_rows) for var in self.variables]
        self.data = {var.name:var.data for var in self.variables}
        #self.clear_memory()
        
    # Process question data
    def process_question(self, q):
        # get the question data
        qdata = q._output_data()
        
        # create new variables if needed
        [self.create_var(name,data,q._all_rows) 
            for (name,data) in qdata.items()]
            
        # get list of relevant variables
        vars = Variable.query.filter(
            and_(Variable.part_id==self.id,
                Variable.name.in_(qdata.keys())))
        vars = vars.order_by('name').all()
        
        # pad existing variables so question writes to same row
        max_rows = max(v.num_rows for v in vars)
        [var.pad(max_rows) for var in vars]
        
        # write data to variables
        [var.add_data(qdata[name]) for name,var in zip(sorted(qdata),vars)]
        
    # Create a new variable if needed
    def create_var(self, name, data, all_rows):
        if name in [var.name for var in self.variables]:
            return
        var = Variable(part=self, name=name, all_rows=all_rows)
        
    # Clear branches, pages, and questions from database
    def clear_memory(self):
        [db.session.delete(b) for b in Branch.query.filter_by(part_id=self.id).all()]
        [db.session.delete(p) for p in Page.query.filter_by(part_id=self.id).all()
            if p != self.curr_page]
        [db.session.delete(q) for q in Question.query.filter_by(part_id=self.id).all() 
            if q not in self.curr_page.questions]
        db.session.commit()