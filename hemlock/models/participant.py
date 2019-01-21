###############################################################################
# Participant model
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import db
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable

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
    def __init__(self):
        db.session.add(self)
        db.session.commit()
        
    # Return current page
    def get_page(self):
        return self.curr_page
        
    # Advance to next page
    # inspects branch at top of stack
    # removes next page from the branch's page queue
    # terminates branch if page queue is empty
    # updates current page
    def advance_page(self):
        if not self.branch_stack.all():
            return False
        branch = self.branch_stack[-1]
        page = branch.dequeue()
        if page is None:
            self.terminate_branch(branch)
            return self.advance_page()
        self.curr_page = page
        return True
        
    # Terminate a branch
    # if current branch points to next branch, add next branch to branch stack
    def terminate_branch(self, branch):
        new_branch = branch.get_next()
        self.branch_stack.remove(branch)
        if new_branch is not None:
            new_branch.part = self
            
    # Store participant data
    # processes data from each question the participant answered
    # pads variables so they are all of equal length
    # clears branches, pages, and questions from database
    def store_data(self):
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