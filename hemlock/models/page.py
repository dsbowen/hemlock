"""Page database model

"""

from hemlock.factory import attr_settor, compiler, db
from hemlock.models.question import Question
from hemlock.models.private.base import Base, iscallable
from flask import request
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from datetime import datetime



'''
Relationships:
    branch: branch to whose queue this page belongs
    next_branch: child branch which originated from this page
    questions: list of questions
    start_time: time at which this page was last rendered
    timer: question to track time spent on this page
    forward_to: page to which this page navigates forward
    back_to: page to which this page navigates back

Columns:
    back: indicates that page has back button
    terminal: indicates that page is terminal (last in the survey)
    
    compile: function called when page html is compiled
    compile_args: arguments for compile function
    post: function called after page is submitted (posted)
    post_args: arguments for post function
    next: navigation function which grows the next branch
    next_args: arguments for next function
    debug: debug function called by AI Participant
    debug_args: arguments for debug function
    
    compiled: indicates that the page has been compiled
    direction_to: direction to which this page was navigated
    direction_from: direction from which the page navigates
'''
class Page(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _branch_head_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    index = db.Column(db.Integer)

    next_branch = db.relationship(
        'Branch',
        back_populates='origin_page',
        uselist=False,
        foreign_keys='Branch._origin_page_id'
        )
    
    questions = db.relationship(
        'Question', 
        backref='page',
        order_by='Question.index',
        collection_class=ordering_list('index'),
        foreign_keys='Question._page_id'
        )
        
    start_time = db.Column(db.DateTime)
    timer = db.relationship(
        'Question',
        uselist=False,
        foreign_keys='Question._page_timer_id'
        )
        
    _forward_to_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    forward_to = db.relationship(
        'Page', 
        uselist=False, 
        foreign_keys=_forward_to_id)
        
    _back_to_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    back_to = db.relationship(
        'Page', 
        uselist=False, 
        foreign_keys=_back_to_id)
    
    back = db.Column(db.Boolean)
    terminal = db.Column(db.Boolean)
    
    compile = db.Column(db.PickleType)
    compile_args = db.Column(db.PickleType)
    post = db.Column(db.PickleType)
    post_args = db.Column(db.PickleType)
    next = db.Column(db.PickleType)
    next_args = db.Column(db.PickleType)
    debug = db.Column(db.PickleType)
    debug_args = db.Column(db.PickleType)
    
    compiled = db.Column(db.Boolean, default=False)
    direction_to = db.Column(db.String(8))
    direction_from = db.Column(db.String(8))
    
    
    
    # Initialization
    def __init__(
            self, branch=None, index=None,
            timer_var=None, all_rows=False,
            back=False, terminal=False, 
            compile=None, compile_args={},
            post=None, post_args={},
            next=None, next_args={},
            debug=None, debug_args={},
            forward_to=None, back_to=None):
        
        db.session.add(self)
        db.session.flush([self])
        
        self.set_branch(branch, index)
        self.timer = Question(data=0, var=timer_var, all_rows=all_rows)
        self.back = back
        self.terminal = terminal
        self.compile, self.compile_args = compile, compile_args
        self.post, self.post_args = post, post_args
        self.next, self.next_args = next, next_args
        self.debug, self.debug_args = debug, debug_args
        self.forward_to, self.back_to = forward_to, back_to



    ##########################################################################
    # Public methods
    ##########################################################################
    
    # Set branch to which this page belongs
    def set_branch(self, branch, index):
        self._set_parent(branch, index, 'branch', 'pages')
    
    # Reset page timer
    def reset_timer(self):
        self.timer.data = 0

    # Return whether page submission was valid
    def valid(self):
        return not any([q.error for q in self.questions])
    
    # Return whether page is blank
    def blank(self):
        return all([q.response in [None, ''] for q in self.questions])
    
    
    ##########################################################################
    # Private methods
    ##########################################################################
    
    # Order of major operations for html compilation and page submission:
        # set direction to which this page was navigated
        # execute compile functions (page then question)
        # compile html
        # get requested direction from form
        # record participant responses
        # execute post functions (question then page)
        # navigate in appropriate direction
            # if direction from is back, return back
            # if responses are not valid, repeat page
            # if responses are valid, go forward
    
    # Compile html for the form specified on this page
    # set direction from which this page was navigated to
    # execute compile functions (page then question)
    # return compiled html
    def _compile_html(self, direction_to):
        self.direction_to = direction_to
    
        self._call_function(self.compile, self.compile_args, self)
        [q._call_function(q.compile, q.compile_args, q) 
            for q in self.questions]
        
        html = compiler.compile_page(self)
        self.compiled = True
        self.start_time = datetime.utcnow()
        return html
        
    # Check if questions have valid answers upon page submission
    # get requested direction from form
    # record participant responses
    # execute post functions (question then page)
    # navigate in appropriate direction
    def _validate_on_submit(self):
        self._update_timer()
        self.direction_from = request.form.get('direction')

        [q._record_response(request.form.get('q'+str(q.id))) 
            for q in self.questions if q.qtype != 'embedded']

        [q._call_function(q.post, q.post_args, q)
            for q in self.questions]
        self._call_function(self.post, self.post_args, self)
        
        return self._navigate()
        
    # Update the page timer
    def _update_timer(self):
        if self.start_time is None:
            self.start_time = datetime.utcnow()
        delta = (datetime.utcnow() - self.start_time).total_seconds()
        self.timer.data += delta
    
    # Navigate from page
    def _navigate(self):
        if self.direction_from == 'back':
            return 'back'
        if not all([q._validate() for q in self.questions]):
            self.direction_to = self.direction_from = 'invalid'
            return 'invalid'
        return 'forward'

# Validate function attributes are callable (or None)
@attr_settor.register(Page, ['compile','post','next','debug'])
def valid_function(page, value):
    return iscallable(value)
    
# Validate direction variables
@attr_settor.register(Page, ['direction_to', 'direction_from'])
def valid_direction(page, value):
    if value not in [None, 'forward', 'back', 'invalid']:
        raise ValueError("Direction must be 'forward', 'back', or 'invalid'")
    return value