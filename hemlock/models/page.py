###############################################################################
# Page model
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from flask import request
from hemlock import db
from hemlock.models.question import Question
from hemlock.models.base import Base
from random import choice
from string import ascii_letters, digits

# Create a hidden tag for form (for security purposes)
def hidden_tag():
    tag = ''.join([choice(ascii_letters + digits) for i in range(90)])
    return "<input name='crsf_token' type='hidden' value='{0}'>".format(tag)
    
# Submit button
def submit(page):
    if page.terminal:
        return ''
    return '''
        <p align=right><input type='submit' name='submit' value='>>'></p>
        '''

# Data:
# ID of participant to whom the page belongs
# ID of branch to which the page belongs
# List of questions
# Indicator of whether form submission is valid
# Indicator of whether this page is terminal
# Order in which the page appears in its branch
class Page(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    questions = db.relationship('Question', backref='page', lazy='dynamic')
    valid = db.Column(db.Boolean, default=False)
    terminal = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer)
    next = db.Column(db.PickleType)
    next_args = db.Column(db.PickleType)
    render_function = db.Column(db.PickleType)
    render_args = db.Column(db.PickleType)
    post_function = db.Column(db.PickleType)
    post_args = db.Column(db.PickleType)
    rendered = db.Column(db.Boolean, default=False)
    
    # Add to database and commit upon initialization
    def __init__(self, branch=None, order=None, terminal=False, next=None, next_args=None, render=None, render_args=None, post=None, post_args=None):
        self.assign_branch(branch, order)
        self.set_terminal(terminal)
        self.set_next(next, next_args)
        self.set_render(render, render_args)
        self.set_post(post, post_args)
        db.session.add(self)
        db.session.commit()
    
    # Assign to branch
    # page to is assigned to end of queue by default
    def assign_branch(self, branch, order=None):
        if branch is not None:
            self.assign_parent('branch', branch, branch.page_queue.all(), order)
        
    # Remove from branch
    def remove_branch(self):
        if self.branch is not None:
            self.remove_parent('branch', self.branch.page_queue.all())
        
    # Indicates whether the page is terminal
    def set_terminal(self, terminal=True):
        self.terminal = terminal
    
    # Render the html code for the form specified on this page
    # renders html for each question in Qhtml
    # adds a hidden tag and submit button
    def render_html(self):
        if not self.rendered:
            self.rendered = True
            self.call_function(self, self.render_function, self.render_args)
        Qhtml = [q.render_html() for q in self.questions.order_by('order')]
        db.session.commit()
        return ''.join([hidden_tag()]+Qhtml+[submit(self)])
        
    # Checks if questions have valid answers upon page submission
    def validate_on_submit(self):
        [q.record_entry(request.form.get(str(q.id))) for q in self.questions
            if q.qtype != 'embedded']
        valid = all([q.validate() for q in self.questions])
        self.call_function(self, self.post_function, self.post_args)
        questions = self.questions.order_by('order')
        [q.call_function(q, q.post_function, q.post_args) for q in questions]
        if valid:
            [q.assign_participant(self.part) for q in self.questions]
        return valid