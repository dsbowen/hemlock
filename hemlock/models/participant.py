###############################################################################
# Participant model
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from datetime import datetime
from hemlock import db
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable
from flask import request

# Data:
# Stack of Branches
# Current Page
# List of Questions
# List of Variables
# Number of rows contributed to dataset
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_stack = db.relationship('Branch', backref='part', lazy='dynamic')
    curr_page = db.relationship('Page', uselist=False, backref='part')
    questions = db.relationship('Question', backref='part', lazy='dynamic')
    variables = db.relationship('Variable', backref='part', lazy='dynamic')
    num_rows = db.Column(db.Integer, default=0)
    
    # Add participant to database and commit on initialization
    # also initialize participant id and start time questions
    def __init__(self): 
        db.session.add(self)
        db.session.commit()
        
        id = Question(var='id', data=self.id, all_rows=True)
        id.part = self
        ip = Question(var='ip_address', data=request.remote_addr, all_rows=True)
        ip.part = self
        ip2 = Question(var='ip_address2', data=request.environ['HTTP_X_FORWARDED_FOR'], all_rows=True)
        ip2.part = self
        ip3 = Question(var='ip3', data=request.envion['HTTP_X_FORWARDED'], all_rows=True)
        ip3.part = self
        ip4 = Question(var='ip4', data=request.environ['HTTP_X_CLIENT_IP'], all_rows=True)
        ip4.part = self
        ip5 = Question(var='ip5', data=request.environ['HTTP_X_CLUSTER_CLIENT_IP'], all_rows=True)
        ip5.part=self
        start = Question(var='start_time', data=datetime.utcnow(), all_rows=True)
        start.part = self
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
        if self.curr_page is not None and self.curr_page.next is not None:
            new_branch = self.curr_page.get_next()
            new_branch.part = self
        branch = self.branch_stack[-1]
        self.curr_page = branch.dequeue()
        if self.curr_page is None:
            self.terminate_branch(branch)
            return self.advance_page()
        
    # Terminate a branch
    # if current branch points to next branch, add next branch to branch stack
    def terminate_branch(self, branch):
        new_branch = branch.get_next()
        self.branch_stack.remove(branch)
        if new_branch is not None:
            new_branch.part = self
            
    # Store participant data
    # add end time variable
    # processes data from each question the participant answered
    # pads variables so they are all of equal length
    # clears branches, pages, and questions from database
    def store_data(self):
        # end = Question.query.filter_by(part_id=self.id, var='end_time').first()
        # self.end.set_data(datetime.utcnow())
        for question in self.questions:
            if question.var:
                self.process_question(question)
        for var in self.variables:
            var.pad(self.num_rows)
        self.clear_memory()
        
    # Process question data
    # if question belongs to a new variable, create a new variable
    # add question data to variable
    def process_question(self, question):
        var = Variable.query.filter_by(part_id=self.id, name=question.var).first()
        if not var:
            var = Variable(part=self, name=question.var, all_rows=question.all_rows)
        var.add_data(question.data)
        
    # Clear branches, pages, and questions from database
    def clear_memory(self):
        for branch in Branch.query.filter_by(part_id=self.id).all():
            db.session.delete(branch)
        for page in Page.query.filter_by(part_id=self.id).all():
            if page != self.curr_page:
                db.session.delete(page)
        for question in Question.query.filter_by(part_id=self.id).all():
            if question not in self.curr_page.questions:
                db.session.delete(question)
        db.session.commit()