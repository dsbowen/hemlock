###############################################################################
# Page model
# by Dillon Bowen
# last modified 02/12/2019
###############################################################################

from hemlock import db
from hemlock.models.question import Question
from hemlock.models.base import Base
from flask import request
from random import choice
from string import ascii_letters, digits

# Create a hidden tag for form (for security purposes)
def hidden_tag():
    tag = ''.join([choice(ascii_letters + digits) for i in range(90)])
    return "<input name='crsf_token' type='hidden' value='{0}'>".format(tag)
    
# Submit button
def submit(page):
    if page._terminal:
        return ''
    return '''
        <p align=right><input type='submit' name='submit' value='>>'></p>
        '''
'''
Data:
_part_id: ID of participant to whom the page belongs
_branch_id: ID of the branch to which the page belongs
_questions: list of questions on this page
_order: order in which the page appears in its branch
_render_function: function called before redering the page
_render_args: arguments for the render function
_post_function: function called after responses are submitted and validated
_post_args: arguments for the post function
_next_function: next navigation function
_next_args: arguments for the next navigation function
_terminal: indicator that the page is the last in the survey
_randomize: indicator of question randomization
_rendered: indicator that the page was previously rendered
'''
class Page(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _questions = db.relationship('Question', backref='_page', lazy='dynamic')
    _order = db.Column(db.Integer)
    _render_function = db.Column(db.PickleType)
    _render_args = db.Column(db.PickleType)
    _post_function = db.Column(db.PickleType)
    _post_args = db.Column(db.PickleType)
    _next_function = db.Column(db.PickleType)
    _next_args = db.Column(db.PickleType)
    _terminal = db.Column(db.Boolean)
    _randomize = db.Column(db.Boolean)
    _rendered = db.Column(db.Boolean, default=False)
    
    # Add to database and commit upon initialization
    def __init__(self, branch=None, order=None,
        render=None, render_args=None,
        post=None, post_args=None,
        next=None, next_args=None,
        terminal=False, randomize=False):
        
        self.assign_branch(branch, order)
        self.set_render(render, render_args)
        self.set_post(post, post_args)
        self.set_next(next, next_args)
        self.set_terminal(terminal)
        self.set_randomize(randomize)
        
        db.session.add(self)
        db.session.commit()
    
    # Assign to branch
    def assign_branch(self, branch, order=None):
        if branch is not None:
            self._assign_parent('_branch', branch, branch._page_queue.all(), order)
        
    # Remove from branch
    def remove_branch(self):
        if self._branch is not None:
            self._remove_parent('_branch', self._branch._page_queue.all())
            
    # Sets the render function and arguments
    def set_render(self, render=None, args=None):
        self._set_function('_render_function', render, '_render_args', args)
        
    # Sets the post function and arguments
    def set_post(self, post=None, args=None):
        self._set_function('_post_function', post, '_post_args', args)
        
    # Sets the next navigation function and arguments
    def set_next(self, next=None, args=None):
        self._set_function('_next_function', next, '_next_args', args)
        
    # Sets the terminal status (i.e. whether this page ends the survey)
    def set_terminal(self, terminal=True):
        self._terminal = terminal
            
    # Set question randomization on/off (True/False)
    def set_randomize(self, randomize=True):
        self._randomize = randomize    
    
    # Render the html code for the form specified on this page
    # executes command on first rendering
    # renders html for each question in Qhtml
    # adds a hidden tag and submit button
    def _render_html(self):
        self._first_render(self._questions.all())
        Qhtml = [q._render_html() for q in self._questions.order_by('_order')]
        self._rendered = True
        db.session.commit()
        return ''.join([hidden_tag()]+Qhtml+[submit(self)])
        
    # Checks if questions have valid answers upon page submission
    def _validate_on_submit(self):
        [q._record_entry(request.form.get(str(q.id))) for q in self._questions
            if q._qtype != 'embedded']
        valid = all([q._validate() for q in self._questions])
        self._call_function(self, self._post_function, self._post_args)
        questions = self._questions.order_by('_order')
        [q._call_function(q, q._post_function, q._post_args) for q in questions]
        if valid:
            [q._assign_participant(self._part) for q in self._questions]
        return valid