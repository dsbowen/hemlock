###############################################################################
# Page model
# by Dillon Bowen
# last modified 03/20/2019
###############################################################################

from hemlock.factory import db
from hemlock.models.question import Question
from hemlock.models.private.base import Base
from hemlock.models.private.html_compiler import *
from flask import request
from flask_login import current_user
from datetime import datetime



'''
Relationships:
    part: participant to whom this page belongs
    branch: branch to whose queue this page belongs
    next_branch: child branch which originated from this page
    forward_to: page to which this page navigates forward
    back_to: page to which this page navigates back
    questions: list of questions
    start_time: time at which this page was rendered (used by timer)
    timer: question to track time spent on this page

Columns:
    back: indicates that page has back button
    terminal: indicates that page is terminal (last in the survey)
    compiled: indicates that the page has been compiled
    
    compile_function: function called when page html is compiled
    compile_args: arguments for compile function
    post_function: function called after page is submitted (posted)
    post_args: arguments for post function
    next_function: navigation function which grows the next branch
    next_args: arguments for next function
    
    direction_to: direction to which this page is arrived at
    direction_from: direction from which the page navigates
'''
class Page(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _branch_head_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _index = db.Column(db.Integer)

    _next_branch = db.relationship(
        'Branch',
        back_populates='_origin_page',
        uselist=False,
        foreign_keys='Branch._origin_page_id')
    
    _questions = db.relationship(
        'Question', 
        backref='_page', 
        lazy='dynamic',
        order_by='Question._index',
        foreign_keys='Question._page_id')
        
    _start_time = db.Column(db.DateTime)
    _timer = db.relationship(
        'Question',
        uselist=False,
        foreign_keys='Question._page_timer_id')
    
    _back = db.Column(db.Boolean)
    _terminal = db.Column(db.Boolean)
    _compiled = db.Column(db.Boolean, default=False)
    
    _compile_function = db.Column(db.PickleType)
    _compile_args = db.Column(db.PickleType)
    _post_function = db.Column(db.PickleType)
    _post_args = db.Column(db.PickleType)
    _next_function = db.Column(db.PickleType)
    _next_args = db.Column(db.PickleType)
    
    _direction_to = db.Column(db.String(8))
    _direction_from = db.Column(db.String(8))
    
    _forward_to_id = db.Column(db.Integer)
    _back_to_id = db.Column(db.Integer)
    
    
    
    # Initialize page
    def __init__(
            self, branch=None, index=None, part=None,
            back=False, terminal=False, timer=None, all_rows=False,
            compile=None, compile_args=None,
            post=None, post_args=None,
            next=None, next_args=None,
            direction_to=None, direction_from=None,
            forward_to=None, back_to=None):
        
        db.session.add(self)
        db.session.commit()
        
        self.timer(timer)
        self.participant(part)
        self.branch(branch, index)
        
        self.back(back)
        self.terminal(terminal)
        self.all_rows(all_rows)
        
        self.compile(compile, compile_args)
        self.post(post, post_args)
        self.next(next, next_args)
        
        self.direction_to(direction_to)
        self.direction_from(direction_from)
        
        self.forward_to(forward_to)
        self.back_to(back_to)



    ###########################################################################
    # Assign and remove parents
    ###########################################################################
    
    # PARTICIPANT
    # Assign page, its questions, and its timer to participant
    def participant(self, participant=current_user):
        self._part = participant
        [q.participant(participant) for q in self._questions]
        self._timer.participant(participant)
        
    # Get participant
    def get_participant(self):
        return self._part
        
    # Remove page, its questions, and its timer from participant
    def remove_participant(self):
        self._part = None
        [q.remove_participant() for q in self._questions.all()]
        self._timer.remove_participant()
        
        
    # BRANCH
    # Assign to branch
    def branch(self, branch, index=None):
        self._assign_parent(branch, '_branch', index)
        
    # Get branch
    def get_branch(self):
        return self._branch
        
    # Get index (position within branch)
    def get_index(self):
        return self._index
        
    # Remove from branch
    def remove_branch(self):
        self._remove_parent('_branch')
    
    
    
    ###########################################################################
    # Insert and remove children
    ###########################################################################
    
    # FORWARD TO AND BACK TO PAGES
    # Set forward_to page
    # to clear, forward_to()
    def forward_to(self, page=None):
        if page is None:
            self._forward_to_id = None
            return
        self._forward_to_id = page.id
        
    # Get forward to page
    def get_forward_to(self):
        return Page.query.get(self._forward_to_id)
        
    # Set back to page
    def back_to(self, page=None):
        if page is None:
            self._back_to_id = None
            return
        self._back_to_id = page.id
    
    # Get back to page
    def get_back_to(self):
        return Page.query.get(self._back_to_id)
    
    
    # QUESTIONS
    # Get list of questions
    def get_questions(self):
        return self._questions.all()
        
    # Clear questions
    def clear_questions(self):
        self._remove_children('_questions')
    
    
    
    ###########################################################################
    # Public methods for manipulating columns
    ###########################################################################
    
    # BACK
    # Set the back button
    # in general, True = on, False = off
    def back(self, back=True):
        self._back = back
        
    # Get the back button status
    def get_back(self):
        return self._back
    
    
    # TERMINAL
    # Set the terminal status (i.e. whether this page ends the survey)
    def terminal(self, terminal=True):
        self._terminal = terminal
        
    # Get the terminal status
    def get_terminal(self):
        return self._terminal
    
    
    # COMPILED
    # Get compiled indicator (whether the page was compiled)
    def get_compiled(self):
        return self._compiled
    
        
    # TIMER
    # Set the timer variable
    def timer(self, var=None):
        if self._timer is None:
            self._timer = Question(data=0)
        self._timer.var(var)
        
    # Reset timer to 0
    def reset_timer(self):
        self._timer.data(0)
    
    # Sets all_rows indicator for timer
    # i.e. timer data will appear in all of participant's rows
    def all_rows(self, all_rows=True):
        self._timer.all_rows(all_rows)
    
    
    # COMPILE FUNCTION AND ARGUMENTS  
    # Set the compile function and arguments
    # to clear function and args, compile()
    def compile(self, compile=None, args=None):
        self._set_function('_compile_function', compile, '_compile_args', args)
        
    # Return the compile function
    def get_compile(self):
        return self._compile_function
        
    # Return the compile function arguments
    def get_compile_args(self):
        return self._compile_args
        
        
    # POST FUNCTION AND ARGUMENTS
    # Set the post function and arguments
    def post(self, post=None, args=None):
        self._set_function('_post_function', post, '_post_args', args)
        
    # Return the post function
    def get_post(self):
        return self._post_function
        
    # Return the post function arguments
    def get_post_args(self):
        return self._post_args
    
    
    # NEXT FUNCTION AND ARGUMENTS
    # Set the next navigation function and arguments
    def next(self, next=None, args=None):
        self._set_function('_next_function', next, '_next_args', args)
        
    # Get the next function
    def get_next(self):
        return self._next_function
        
    # Get the next function arguments
    def get_next_args(self):
        return self._next_args

        
    # DIRECTION
    # Set direction for page and its questions
    def direction_to(self, direction=None):
        self._direction_to = direction
        
    def direction_from(self, direction=None):
        self._direction_from = direction
        
    # Get direction
    def get_direction_to(self):
        return self._direction_to
        
    def get_direction_from(self):
        return self._direction_from
    
    
    # RANDOMIZATION
    # Randomize order or questions
    def randomize(self):
        self._randomize_children('_questions')
    
    
    
    ###########################################################################
    # Private functions
    ###########################################################################
    
    # Order of major operations for html compilation and page submission:
        # execute compile functions (page then question)
        # render html
        # set direction from
        # record participant responses
        # execute post functions (question then page)
        # navigate in appropriate direction
            # if direction from is back, return back
            # if responses are not valid, repeat page
            # if responses are valid, go forward
    
    # Compile the html code for the form specified on this page
    # executes compile functions (page then question)
    # returns compiled html with hidden tag and submit button
    def _compile_html(self):
        self._call_function(self, self._compile_function, self._compile_args)
        [q._call_function(q, q._compile_function, q._compile_args)
            for q in self._questions]
        
        Qhtml = [q._compile_html() for q in self._questions]
        self._compiled = True
        self._start_time = datetime.utcnow()
        db.session.commit()
        return ''.join([hidden_tag()]+Qhtml+[submit(self)])
        
    # Checks if questions have valid answers upon page submission
    # set direction from
    # record participant responses
    # execute post functions (question then page)
    # navigate in appropriate direction
    def _validate_on_submit(self):
        self._update_timer()
        self.direction_from(request.form.get('direction'))

        [q._record_response(request.form.get(str(q.id))) 
            for q in self._questions if q._qtype != 'embedded']

        [q._call_function(q, q._post_function, q._post_args)
            for q in self._questions]
        self._call_function(self, self._post_function, self._post_args)
            
        if self._direction_from == 'back':
            return 'back'
        if not all([q._validate() for q in self._questions]):
            self.direction_to('invalid')
            self.direction_from('invalid')
            return 'invalid'
        return 'forward'
        
    # Update the page timer
    def _update_timer(self):
        delta = (datetime.utcnow() - self._start_time).total_seconds()
        self._timer.data(self._timer.get_data() + delta)