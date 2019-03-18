###############################################################################
# Page model
# by Dillon Bowen
# last modified 03/18/2019
###############################################################################

from hemlock.factory import db
from hemlock.models.question import Question
from hemlock.models.private.base import Base
from flask import request
from flask_login import current_user
from datetime import datetime
from random import choice
from string import ascii_letters, digits

# Create a hidden tag for form (for security purposes)
def hidden_tag():
    return '''
    <div class='form-group'
        <input name='crsf_token' type='hidden' value='{0}'>
    </div>
    '''.format(''.join([choice(ascii_letters + digits) for i in range(90)]))
    
# Submit button
def submit(page):
    html = '<br></br>'
    if page._back:
        html += '''
    <button name='direction' type='submit' class='btn btn-primary' style='float: left;' value='back'> 
    << 
    </button>
    '''
    if page._terminal:
        return html+"<br style = 'line-height:3;'></br>"
    return html + '''
    <button name='direction' type='submit' class='btn btn-primary' style='float: right;' value='forward'>
    >> 
    </button>
    <br style = 'line-height:3;'></br>
    '''
        
'''
Relationships:
    branch: branch to whose queue this page belongs
    next_branch: child branch which originated from this page
    questions: list of questions
    timer: question to track time spent on this page

Columns:
    start_time: time at which this page was rendered (used by timer)
    compile_function: function called when page html is compiled
    compile_args: arguments for compile function
    post_function: function called after page is submitted (posted)
    post_args: arguments for post function
    next_function: navigation function which grows the next branch
    next_args: arguments for next function

    back: indicates that page has back button
    terminal: indicates that page is terminal (last in the survey)
    compiled: indicates that the page has been compiled
    assigned_to_participant: indicates that page has been assigned to part
    
    direction_to: direction to which this page is arrived at
    direction_from: direction from which the page navigates
'''
class Page(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
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
        index_by='Question._index',
        foreign_keys='Question._page_id')
        
    _start_time = db.Column(db.DateTime)
    _timer = db.relationship(
        'Question',
        uselist=False,
        foreign_keys='Question._page_timer_id')
    
    _compile_function = db.Column(db.PickleType)
    _compile_args = db.Column(db.PickleType)
    _post_function = db.Column(db.PickleType)
    _post_args = db.Column(db.PickleType)
    _next_function = db.Column(db.PickleType)
    _next_args = db.Column(db.PickleType)
    
    _back = db.Column(db.Boolean)
    _terminal = db.Column(db.Boolean)
    _compiled = db.Column(db.Boolean, default=False)
    _assigned_to_participant = db.Column(db.Boolean, default=False)
    
    _direction_to = db.Column(db.String(8))
    _direction_from = db.Column(db.String(8))
    
    
    
    # Initialize page
    def __init__(
            self, branch=None, index=None, 
            back=False, terminal=False, timer=None,
            compile=None, compile_args=None,
            post=None, post_args=None,
            next=None, next_args=None):
        
        db.session.add(self)
        db.session.commit()
        
        self.branch(branch, index)
        self.compile(compile, compile_args)
        self.post(post, post_args)
        self.next(next, next_args)
        self.back(back)
        self.terminal(terminal)

        self._timer = Question(var=timer, data=0)
        
    # Assign to participant
    def participant(self, participant=current_user):
        self._assigned_to_participant = True
        [q.participant(participant) for q in self._questions.all()]
        self._timer.participant(participant)
        
    # Remove from participant
    def remove_participant(self):
        self._assigned_to_participant = False
        [q.remove_participant() for q in self._questions.all()]
        self._timer.remove_participant()
    
    # Assign to branch
    def branch(self, branch, index=None):
        self._assign_parent(branch, '_branch', index)
        
    # Remove from branch
    def remove_branch(self):
        self._remove_parent('_branch')
            
    # Set the compile function and arguments
    def compile(self, compile=None, args=None):
        self._set_function('_compile_function', compile, '_compile_args', args)
        
    # Set the post function and arguments
    def post(self, post=None, args=None):
        self._set_function('_post_function', post, '_post_args', args)
        
    # Set the next navigation function and arguments
    def next(self, next=None, args=None):
        self._set_function('_next_function', next, '_next_args', args)
        
    # Set the back button
    def back(self, back=True):
        self._back = back
        
    # Set the terminal status (i.e. whether this page ends the survey)
    def terminal(self, terminal=True):
        self._terminal = terminal
            
    # Randomize question index
    def randomize(self):
        self._randomize_children(self._questions.all())
        
    # Get the direction (forward, back, or invalid)
    # from which this page was arrived at
    def get_direction_to(self):
        return self._direction_to
        
    # Set the navigation direction (forward, back, or invalid)
    # from which this page is arrived at
    def _set_direction_to(self, direction):
        self._direction_to = direction
    
    # Compile the html code for the form specified on this page
    # executes compile functions for page and questions
    # returns compiled html with hidden tag and submit button
    def _compile_html(self):
        # page compile function
        self._call_function(self, self._compile_function, self._compile_args)
        
        # question compile functions
        [q._call_function(q, q._render_function, q._render_args)
            for q in self._questions]
        
        # compile html
        Qhtml = [q._render_html() for q in self._questions]
        self._compiled = True
        self._start_time = datetime.utcnow()
        db.session.commit()
        return ''.join([hidden_tag()]+Qhtml+[submit(self)])
        
    # Checks if questions have valid answers upon page submission
    def _validate_on_submit(self):
        self._update_timer()

        # set direction from
        self._direction_from = request.form.get('direction')
        
        # record responses
        [q._record_response(request.form.get(str(q.id))) 
            for q in self._questions if q._qtype != 'embedded']
            
        # question post functions
        [q._call_function(q, q._post_function, q._post_args) 
            for q in self._questions]
            
        # page post function
        self._call_function(self, self._post_function, self._post_args)
            
        # back navigation
        if self._direction_from == 'back':
            return 'back'
            
        # validate
        valid = all([q._validate() for q in self._questions])
        
        # invalid navigation
        if not valid:
            self._direction_to = self._direction_from = 'invalid'
            return 'invalid'
            
        # forward navigation
        return 'forward'
        
    # Update the page timer
    def _update_timer(self):
        delta = (datetime.utcnow() - self._start_time).total_seconds()
        self._timer.data(self._timer.get_data() + delta)