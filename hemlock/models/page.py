###############################################################################
# Page model
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

from hemlock.factory import db
from hemlock.models.question import Question
from hemlock.models.checkpoint import Checkpoint
from hemlock.models.base import Base
from flask import request
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
Data:
_branch_id: ID of the branch to which the page belongs
_questions: list of questions on this page
_order: order in which the page appears in its branch
_compile_function: function called before redering the page
_compile_args: arguments for the compile function
_post_function: function called after responses are submitted and validated
_post_args: arguments for the post function
_next_function: next navigation function
_next_args: arguments for the next navigation function
_back: indicator for back button
_id_next: ID of the next branch
_terminal: indicator that the page is the last in the survey
_randomize: indicator of question randomization
_compileed: indicator that the page was previously compileed
_restore_on: dictionary of restoration states
    'forward': 0, 1, or 2
    'back': 1 or 2
    'invalid'; 1 or 2
_state: integer representing the current state
    0 - before compile functions
    1 - after compile functions, before response collection
    2 - after response collection
_state_copy_ids: list of state copy ids
_direction: direction of survey flow - forward, back, invalid
_compiled: indicator that the page was previously compiled
_checkpoint: indicates that the page is a checkpoint
'''
class Page(db.Model, Checkpoint, Base):
    # primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # parent foreign keys and order
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _queue_order = db.Column(db.Integer)
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _order = db.Column(db.Integer)
    
    # children
    _questions = db.relationship('Question', backref='_page', lazy='dynamic',
        order_by='Question._order')
        
    # timing variables
    _timer = db.Column(db.Integer) # SHOULD HAVE A 1:1 RELATIONSHIP
    _start_time = db.Column(db.DateTime)
    _total_time = db.Column(db.Integer, default=0)
    
    # functions and arguments
    _compile_function = db.Column(db.PickleType)
    _compile_args = db.Column(db.PickleType)
    _post_function = db.Column(db.PickleType)
    _post_args = db.Column(db.PickleType)
    _next_function = db.Column(db.PickleType)
    _next_args = db.Column(db.PickleType)
    _id_next = db.Column(db.Integer) # SHOULD HAVE 1:1 RELATIONSHIP
    
    # indicator variables
    _back = db.Column(db.Boolean)
    _terminal = db.Column(db.Boolean)
    _compiled = db.Column(db.Boolean)
    
    # direction
    _direction_to = db.Column(db.String(8), default='forward')
    _direction_from = db.Column(db.String(8), default='forward')
    
    # for use by checkpoints
    _checkpoint = db.Column(db.Boolean, default=False)
    _origin_id = db.Column(db.Integer)
    _origin_table = db.Column(db.PickleType)
    _next_len = db.Column(db.Integer, default=0)
    
    # Add to database and commit upon initialization
    def __init__(self, branch=None, timer=None, order=None,
        compile=None, compile_args=None,
        post=None, post_args=None,
        next=None, next_args=None,
        back=False, terminal=False):
        
        db.session.add(self)
        db.session.commit()
        
        self.branch(branch, order)
        self.compile(compile, compile_args)
        self.post(post, post_args)
        self.next(next, next_args)
        self.back(back)
        self.terminal(terminal)

        timer = Question(var=timer, data=0)
        self._timer = timer.id
    
    # Assign to branch
    def branch(self, branch, order=None):
        self._assign_parent(branch, order)
        
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
            
    # Randomize question order
    def randomize(self):
        self._randomize_children(self._questions.all())
        
    # Return the id of the next branch
    def get_next_branch_id(self):
        return self._id_next
        
    # Get the direction (forward, back, or invalid)
    # from which this page was arrived at
    def get_direction_to(self):
        return self._direction_to
        
    # Set the navigation direction (forward, back, or invalid)
    # from which this page is arrived at
    def _set_direction_to(self, direction):
        self._direction_to = direction
        
    # Set the order in participant's page queue
    def _set_queue_order(self, order):
        self._queue_order = order
        
    # Modify the order in participant's page queue
    def _modify_queue_order(self, modify):
        self._queue_order += modify
        
    # Assign participant
    def _insert_to_queue(self, part_id, queue_order):
        self._part_id, self._queue_order = part_id, queue_order
        
    # Remove participant
    def _remove_from_queue(self):
        self._part_id, self._queue_order = None, None
    
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
    def _validate_on_submit(self, part_id):
        self._update_timer(part_id)

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
            if self._timer is not None:
                timer = Question.query.get(self._timer)
                timer._unassign_participant()
            [q._unassign_participant() for q in self._questions]
            return 'back'
            
        # validate
        valid = all([q._validate() for q in self._questions])
        
        # invalid navigation
        if not valid:
            self._direction_to = 'invalid'
            self._direction_from = 'invalid'
            return 'invalid'
            
        # forward navigation
        [q._assign_participant(part_id) for q in self._questions]
        return 'forward'
        
    # FIX THIS
    def _update_timer(self, part_id):
        delta = (datetime.utcnow() - self._start_time).total_seconds()
        self._total_time += delta
        if self._timer is None:
            return
        timer = Question.query.get(self._timer)
        timer.data(self._total_time)
        timer._assign_participant(part_id)