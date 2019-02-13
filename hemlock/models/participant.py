###############################################################################
# Participant model
# by Dillon Bowen
# last modified 02/12/2019
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
    branch_stack = db.relationship('Branch', backref='_part', lazy='dynamic')
    curr_page = db.relationship('Page', uselist=False, backref='_part')
    questions = db.relationship('Question', backref='_part', lazy='dynamic')
    variables = db.relationship('Variable', backref='part', lazy='dynamic')
    data = db.Column(db.PickleType, default={})
    num_rows = db.Column(db.Integer, default=0)
    
    # Add participant to database and commit on initialization
    # also initialize participant id and start time questions
    def __init__(self, ipv4): 
        db.session.add(self)
        db.session.commit()
        
        id = Question(var='id', data=self.id, all_rows=True)
        id._assign_participant(self)
        ipv4 = Question(var='ipv4', data=ipv4, all_rows=True)
        ipv4._assign_participant(self)
        
        start = Question(var='start_time', data=datetime.utcnow(), all_rows=True)
        start._assign_participant(self)
        # self.end = Question(var='end_time', all_rows=True)
        # self.end.part = self
        # ADD IP ADDRESS, LOCATION, ETC, HERE
        # ALSO HAVE SEPARATE IP ADDRESS TABLE
        
    # Return current page
    def get_page(self):
        return self.curr_page
        
    # Advance forward one page
    # if current page branches off, push that branch
    # inspect the branch on top of the stack
    # dequeue the first page in that branch's queue
    # if there are no more pages in the queue, terminate the branch and advance
    def advance_page(self):
        if self.curr_page is not None and self.curr_page._next_function is not None:
            new_branch = self.curr_page._get_next()
            new_branch._assign_participant(self)
        branch = self.branch_stack[-1]
        self.curr_page = branch._dequeue()
        if self.curr_page is None:
            self.terminate_branch(branch)
            return self.advance_page()
        
    # Terminate a branch
    # if current branch points to next branch, add next branch to branch stack
    def terminate_branch(self, branch):
        new_branch = branch._get_next()
        self.branch_stack.remove(branch)
        if new_branch is not None:
            new_branch._assign_participant(self)
            
    # Store participant data
    # add end time variable
    # processes data from each question the participant answered
    # pads variables so they are all of equal length
    # clears branches, pages, and questions from database
    def store_data(self):
        # end = Question.query.filter_by(part_id=self.id, var='end_time').first()
        # self.end.set_data(datetime.utcnow())
        [self.process_question(q) 
			for q in self.questions.order_by('id') if q._var]
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