"""Page database model

Relationships:

branch: Branch to which this Page belongs
next_branch: Branch to which this Page navigates
back_to: Page to which this Page navigates on 'back'
forward_to: Page to which this Page navigates on 'forward'
questions: list of questions
timer: Question which tracks how long a Participant spent on this page

Public (non-Function) Columns:

back: indicates this Page has a back button
back_button: html for back button
compiled: indicates that this Page has ever been compiled
css: list of css files
direction_from: direction from which this Page is navigating
direction_to: direction to which this Page was navigated
forward: indicates this Page has a forward button
forward_button: html for forward button
js: list of js files
template: name of html template
terminal: indicates this Page is the last in the experiment

Function Columns:

compile: run before html is compiled
debug: run during debugging
navigate: run to create the next Branch to which the experiment navigates
post: run after data are recorded
"""

from hemlock.app import db
from hemlock.database.private import BranchingBase
from hemlock.database.types import Function, FunctionType, MarkupType
from hemlock.database.models.question import Question

from bs4 import BeautifulSoup
from datetime import datetime
from flask import current_app, Markup, render_template, request, url_for
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import MutableListType

DIRECTIONS = ['back', 'forward', 'invalid', None]


class Page(db.Model, BranchingBase):
    id = db.Column(db.Integer, primary_key=True)
    @property
    def pid(self):
        return 'p{}'.format(self.id)
    
    @property
    def part(self):
        return self.branch.part if self.branch is not None else None
    
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _branch_head_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    index = db.Column(db.Integer)

    next_branch = db.relationship(
        'Branch',
        back_populates='origin_page',
        uselist=False,
        foreign_keys='Branch._origin_page_id'
        )
    
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
    
    _navbar_id = db.Column(db.Integer, db.ForeignKey('navbar.id'))
    
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
    
    _back = db.Column(db.Boolean)
    back_button = db.Column(MarkupType)
    css = db.Column(MutableListType)
    _direction_from = db.Column(db.String(8))
    _direction_to = db.Column(db.String(8))
    _forward = db.Column(db.Boolean)
    forward_button = db.Column(MarkupType)
    js = db.Column(MutableListType)
    question_html = db.Column(MarkupType)
    survey_template = db.Column(db.Text)
    terminal = db.Column(db.Boolean)
    view_template = db.Column(db.Text)
    
    @property
    def back(self):
        return self._back and not self.first_page()
    
    @back.setter
    def back(self, back):
        self._back = back
    
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
        
    @property
    def forward(self):
        return self._forward and not self.terminal
    
    @forward.setter
    def forward(self, forward):
        self._forward = forward
    
    compile = db.Column(FunctionType)
    debug = db.Column(FunctionType)
    navigate = db.Column(FunctionType)
    post = db.Column(FunctionType)
    
    def __init__(
            self, branch=None, index=None, back_to=None, forward_to=None, 
            nav=None, questions=[], timer_var=None, all_rows=False,
            back=None, back_button=None, css=None, 
            forward=True, forward_button=None, js=None,
            survey_template=None, terminal=False, view_template=None, 
            compile=None, debug=None, navigate=None, post=None):
        
        BranchingBase.__init__(self)
        
        self.set_branch(branch, index)
        self.back_to = back_to
        self.forward_to = forward_to
        self.nav = nav or current_app.nav
        self.questions = questions
        self.timer = Question(all_rows=all_rows, data=0, var=timer_var)
        
        self.back = current_app.back if back is None else back
        self.back_button = back_button or current_app.back_button
        self.css = css or current_app.css
        self.forward = forward
        self.forward_button = forward_button or current_app.forward_button
        self.js = js or current_app.js
        self.survey_template = survey_template or current_app.survey_template
        self.terminal = terminal
        self.view_template = view_template or current_app.view_template

        self.compile = compile or current_app.page_compile
        self.debug = debug or current_app.page_debug
        self.navigate = navigate
        self.post = post or current_app.page_post

    def set_branch(self, branch, index=None):
        self._set_parent(branch, index, 'branch', 'pages')
    
    def blank(self):
        return all([q.response is None for q in self.questions])
        
    def reset_compile(self):
        compile = default_compile
    
    def reset_post(self):
        post = default_post
        
    def reset_timer(self):
        self.timer.data = 0

    def valid(self):
        return all([q.error is None for q in self.questions])
    
    def first_page(self):
        """Indicate that this is the first Page in the experiment"""
        return (
            self.branch is not None and self.branch._isroot 
            and self.index == 0
            )

    def _compile_question_html(self):
        self.compile(object=self)
        self.question_html = Markup(''.join(
            [q._compile_html() for q in self.questions]))
        self.start_time = datetime.utcnow()
        
    def _render_html(self):
        """Render html from survey template
        
        Compile question html if this has not been done already.
        """
        if self.question_html is None:
            self._compile_question_html()
        return render_template(self.survey_template, page=self)        
        
    def view_html(self):
        """View compiled html for debugging purposes"""
        soup = BeautifulSoup(self.question_html, 'html.parser')
        print(soup.prettify())
        
    def _submit(self):
        """Operations executed on page submission
        
        1. Record responses
        2. If attempting to navigate backward, there is nothing more to do
        3. If attempting to navigate forward, check for valid responses
        4. If responses are invalid, return
        5. Record data
        6. Run post function
        """
        self._update_timer()
        self.direction_from = request.form['direction']
        [q._record_response(request.form.getlist(q.qid)) 
            for q in self.questions]
        
        if self.direction_from == 'back':
            return 'back'
        if not all([q._validate() for q in self.questions]):
            self.direction_from = 'invalid'
            return 'invalid'
        [q._record_data() for q in self.questions]
        self.post(object=self)
        # self.direction_from is 'forward' unless changed in post function
        return self.direction_from 
        
    def _update_timer(self):
        if self.start_time is None:
            self.start_time = datetime.utcnow()
        delta = (datetime.utcnow() - self.start_time).total_seconds()
        self.timer.data += delta
    
    def view_nav(self, indent):
        """Print self and next branch for debugging purposes"""
        HEAD_PART = '<== head page of participant'
        HEAD_BRANCH = '<== head page of branch'
        head_part = HEAD_PART if self == self.part.current_page else ''
        head_branch = HEAD_BRANCH if self == self.branch.current_page else ''
        print(indent, self, head_branch, head_part)
        if self.next_branch in self.part.branch_stack:
            self.next_branch.view_nav()