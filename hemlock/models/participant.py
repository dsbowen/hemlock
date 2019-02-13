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
    def __init__(self): 
        db.session.add(self)
        db.session.commit()
        
        id = Question(var='id', data=self.id, all_rows=True)
        id._assign_participant(self)
        
        self.get_ip()
        
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
    # if question belongs to a new variable, create a new variable
    # add question data to variable
    def process_question(self, q):
        var = Variable.query.filter_by(part_id=self.id, name=q._var).first()
        if not var:
            var = Variable(part=self, name=q._var, all_rows=q._all_rows)
        var.add_data(q._data)
        
    # Stores the participant IP address
    def get_ip(self):
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', None)
        if ip is None:
            ip = request.remote_addr
        else:
            ip = ip.split(',')[0]
        ip_var = Question(var='ip_address', data=ip, all_rows=True)
        ip_var._assign_participant(self)
        
    # Clear branches, pages, and questions from database
    def clear_memory(self):
        [db.session.delete(b) for b in Branch.query.filter_by(part_id=self.id).all()]
        [db.session.delete(p) for p in Page.query.filter_by(part_id=self.id).all()
            if p != self.curr_page]
        [db.session.delete(q) for q in Question.query.filter_by(part_id=self.id).all() 
            if q not in self.curr_page.questions]
        db.session.commit()