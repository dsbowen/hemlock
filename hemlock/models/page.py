###############################################################################
# Page model
# by Dillon Bowen
# last modified 02/14/2019
###############################################################################

from hemlock import db
from hemlock.models.question import Question
from hemlock.models.base import Base, intersection_by_key
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
    if page._back:
        
    return '''
        <p align=right><input type='submit' name='submit' value='>>'></p>
        '''
'''
Data:
_branch_id: ID of the branch to which the page belongs
_questions: list of questions on this page
_order: order in which the page appears in its branch
_render_function: function called before redering the page
_render_args: arguments for the render function
_post_function: function called after responses are submitted and validated
_post_args: arguments for the post function
_next_function: next navigation function
_next_args: arguments for the next navigation function
_back: indicator for back button
_id_next: ID of the next branch
_terminal: indicator that the page is the last in the survey
_randomize: indicator of question randomization
_rendered: indicator that the page was previously rendered
_restore_on: dictionary of restoration states
    'forward': 0, 1, or 2
    'back': 1 or 2
    'invalid'; 1 or 2
_state: integer representing the current state
    0 - before render functions
    1 - after render functions, before response collection
    2 - after response collection
_state_copy_ids: list of state copy ids
_direction: direction of survey flow - forward, back, invalid
'''
class Page(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _questions = db.relationship('Question', backref='_page', lazy='dynamic')
    _order = db.Column(db.Integer)
    _render_function = db.Column(db.PickleType)
    _render_args = db.Column(db.PickleType)
    _post_function = db.Column(db.PickleType)
    _post_args = db.Column(db.PickleType)
    _next_function = db.Column(db.PickleType)
    _next_args = db.Column(db.PickleType)
    _back = db.Column(db.Boolean)
    _id_next = db.Column(db.Integer)
    _terminal = db.Column(db.Boolean)
    _randomize = db.Column(db.Boolean)
    _restore_on = db.Column(db.PickleType)
    _state_num= db.Column(db.Integer)
    _state_copy_ids = db.Column(db.PickleType)
    _direction = db.Column(db.String(8), default='forward')
    
    # Add to database and commit upon initialization
    def __init__(self, branch=None, order=None,
        render=None, render_args=None,
        post=None, post_args=None,
        next=None, next_args=None,
        back=False, terminal=False, randomize=False, 
        restore_on={'forward': 2, 'back': 2, 'invalid': 2}):
        
        self._add_commit()
        
        self.branch(branch, order)
        self.render(render, render_args)
        self.post(post, post_args)
        self.next(next, next_args)
        self.back(back)
        self.terminal(terminal)
        self.randomize(randomize)
        self.restore_on(restore_on)
    
    # Assign to branch
    def branch(self, branch, order=None):
        self._assign_parent(branch, order)
        
    # Remove from branch
    def remove_branch(self):
        self._remove_parent('_branch')
            
    # Sets the render function and arguments
    def render(self, render=None, args=None):
        self._set_function('_render_function', render, '_render_args', args)
        
    # Sets the post function and arguments
    def post(self, post=None, args=None):
        self._set_function('_post_function', post, '_post_args', args)
        
    # Sets the next navigation function and arguments
    def next(self, next=None, args=None):
        self._set_function('_next_function', next, '_next_args', args)
        
    # Set the back button
    def back(self, back=True):
        self._back = back
        
    # Sets the terminal status (i.e. whether this page ends the survey)
    def terminal(self, terminal=True):
        self._terminal = terminal
            
    # Set question randomization on/off (True/False)
    def randomize(self, randomize=True):
        self._randomize = randomize

    # Set directions for restoration
    # takes a dictionary with keys 'forward', 'back', 'invalid'
    # and values as state number (1-2 for back and invalid, 0-2 for forward)
    def restore_on(self, restore_on):
        if self._restore_on is None:
            self._restore_on = {'forward':2,'back':2,'invalid':2}
        temp = self._restore_on
        for direction, state_num in restore_on.items():
            temp[direction] = state_num
        self._restore_on = temp
    
    # Render the html code for the form specified on this page
    # executes command on first rendering
    # renders html for each question in Qhtml
    # adds a hidden tag and submit button
    def _render_html(self):
        # create state copies, store s0
        if self._state_num is None:
            state_copies = [Page(),Page(),Page()]
            self._state_copy_ids = [p.id for p in state_copies]
            self._store_state(0)
        else:
            state_num = self._restore_on[self._direction]
            if self._state_num != state_num:
                self._copy(self._state_copy_ids[state_num])
            
        # render functions
        if self._state_num==0:
            # page render function and question randomization
            self._first_rendition(self._questions.all())
            
            # question render functions and choice randomization
            [q._first_rendition(q._choices.all()) 
                for q in self._questions.order_by('_order')]
                
            # store s1 and s2
            self._store_state(1)
            self._store_state(2)
        
        # html
        Qhtml = [q._render_html() for q in self._questions.order_by('_order')]
        db.session.commit()
        return ''.join([hidden_tag()]+Qhtml+[submit(self)])
        
    # Checks if questions have valid answers upon page submission
    def _validate_on_submit(self, part_id):
        # record responses
        [q._record_response(request.form.get(str(q.id))) 
            for q in self._questions if q._qtype != 'embedded']
            
        # page post function
        self._call_function(self, self._post_function, self._post_args)
        
        # question post functions
        [q._call_function(q, q._post_function, q._post_args) 
            for q in self._questions.order_by('_order')]
            
        # validate
        valid = all([q._validate() for q in self._questions])
        
        # store s2
        self._store_state(2)
        self._store_errors_in_s1()
        
        # assign participant
        if valid:
            [q._assign_participant(part_id) for q in self._questions]
            
        return valid
        
    # Store the current state
    def _store_state(self, state_num):
        self._state_num = state_num
        state = Page.query.get(self._state_copy_ids[state_num])
        state._copy(self.id)
        
    # Store errors from s2 in s1
    def _store_errors_in_s1(self):
        # get states
        s1, s2 = [Page.query.get(self._state_copy_ids[i]) for i in [1,2]]
        
        # get question lists for both states and pair them
        q1, q2 = [state._questions for state in [s1, s2]]
        q1, q2 = intersection_by_key(q1, q2, '_id_orig')
        
        # copy errors
        for i in range(len(q1)):
            q1[i]._error = q2[i]._error