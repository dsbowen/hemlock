"""Page database model

"""

from hemlock.app import db
from hemlock.html import compile_page_body
from hemlock.database.private import BranchingBase
from hemlock.database.types import Function, FunctionType
from hemlock.database.models.question import Question

from bs4 import BeautifulSoup
from datetime import datetime
from flask import request
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import MutableListType

DIRECTIONS = ['back', 'forward', 'invalid', None]
CSS = ['bootstrap.min.css', 'default.min.css']
JS = ['default.min.js']


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
def default_compile_func(page):
    return [q.compile.call(object=q) for q in page.questions]

def default_compile_Function():
    return Function(default_compile_func)

def default_post_func(page):
    return [q.post.call(object=q) for q in page.questions]

def default_post_Function():
    return Function(default_post_func)


class Page(db.Model, BranchingBase):
    id = db.Column(db.Integer, primary_key=True)
    @property
    def pid(self):
        return 'p{}'.format(self.id)
    
    # _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    # _branch_head_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    index = db.Column(db.Integer)

    # next_branch = db.relationship(
        # 'Branch',
        # back_populates='origin_page',
        # uselist=False,
        # foreign_keys='Branch._origin_page_id'
        # )
    
    _back_to_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    back_to = db.relationship(
        'Page', 
        uselist=False, 
        foreign_keys='Page._back_to_id')
        
    _forward_to_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    forward_to = db.relationship(
        'Page', 
        uselist=False, 
        foreign_keys='Page._forward_to_id')
    
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
    
    back = db.Column(db.Boolean)
    compiled = db.Column(db.Boolean, default=False)
    css = db.Column(MutableListType)
    _direction_from = db.Column(db.String(8))
    _direction_to = db.Column(db.String(8))
    forward = db.Column(db.Boolean)
    js = db.Column(MutableListType)
    terminal = db.Column(db.Boolean)
    
    @property
    def direction_from(self):
        return self._direction_from
    
    @direction_from.setter
    def direction_from(self, value):
        assert value in DIRECTIONS, (
            'Direction must be one of: {}'.format(DIRECTIONS)
            )
        self._direction_from = value
        
    @property
    def direction_to(self):
        return self._direction_to
    
    @direction_to.setter
    def direction_to(self, value):
        assert value in DIRECTIONS, (
            'Direction must be one of: {}'.format(DIRECTIONS)
            )
        self._direction_to = value
    
    compile = db.Column(FunctionType)
    debug = db.Column(FunctionType)
    next = db.Column(FunctionType)
    post = db.Column(FunctionType)
    
    def __init__(
            self, branch=None, index=None, back_to=None, forward_to=None, 
            questions=[], timer_var=None, all_rows=False,
            back=False, css=CSS, forward=True, js=JS, terminal=False, 
            compile=default_compile_Function(), 
            debug=Function(), 
            next=Function(), 
            post=default_post_Function()):
        
        db.session.add(self)
        db.session.flush([self])
        
        self.set_branch(branch, index)
        self.back_to = back_to
        self.forward_to = forward_to
        self.questions = questions
        self.timer = Question(data=0, var=timer_var, all_rows=all_rows)
        
        self.back = back
        self.css = css
        self.forward = forward
        self.js = js
        self.terminal = terminal

        self.compile = compile
        self.debug = debug
        self.next = next
        self.post = post

    def set_branch(self, branch, index):
        self._set_parent(branch, index, 'branch', 'pages')
    
    def blank(self):
        return all([q.response is None for q in self.questions])
        
    def reset_compile(self):
        compile = default_compile_Function()
    
    def reset_post(self):
        post = default_post_Function()
        
    def reset_timer(self):
        self.timer.data = 0

    def valid(self):
        return all([q.error is None for q in self.questions])

    def _compile_html(self, direction_to):
        self.direction_to = direction_to
        self.compile.call(object=self)
        self.compiled = True
        self.start_time = datetime.utcnow()
        return compile_page_body(self)
        
    def view_html(self, direction_to='forward'):
        """View compiled html for debugging purposes"""
        soup = BeautifulSoup(self._compile_html(direction_to), 'html.parser')
        print(soup.prettify())
        
    def _submit(self):
        """Operations executed on page submission
        
        1. Record responses
        2. If attempting to navigate backward, there is nothing more to do
        3. If attempting to navigate forward, check for valid responses
        4. If responses are invalid, return this result
        5. If responses are valid, execute post function before returning
        """
        self._update_timer()
        self.direction_from = request.form['direction']
        [q._record_response(request.form.get(q.qid)) for q in self.questions]
        
        if self.direction_from == 'back':
            return 'back'
        if not all([q._validate_response() for q in self.questions]):
            self.direction_from = 'invalid'
            return 'invalid'
        self.post.call(self)
        # self.direction_from is 'forward' unless changed in post function
        return self.direction_from 
        
    def _update_timer(self):
        if self.start_time is None:
            self.start_time = datetime.utcnow()
        delta = (datetime.utcnow() - self.start_time).total_seconds()
        self.timer.data += delta