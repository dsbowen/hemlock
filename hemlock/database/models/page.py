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
from hemlock.database.private import BranchingBase, CompileBase
from hemlock.database.types import  MarkupType
from hemlock.database.models.question import Question

from datetime import datetime
from flask import current_app, Markup, render_template, request, url_for
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import MutableListType

DIRECTIONS = ['back', 'forward', 'invalid', None]


class Page(BranchingBase, CompileBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
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
        foreign_keys='Page._back_to_id'
        )
        
    _forward_to_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    forward_to = db.relationship(
        'Page', 
        uselist=False, 
        foreign_keys='Page._forward_to_id'
        )
    
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
    
    """Function relationships and workers"""
    cache_compile = db.Column(db.Boolean)
    compile_worker = db.Column(db.Boolean)
    _compile_finished = db.Column(db.Boolean, default=False)
    _compile_functions = db.relationship(
        'CompileFunction',
        backref='page',
        order_by='CompileFunction.index',
        collection_class=ordering_list('index')
    )

    _request_method = db.Column(db.String(8))
    _response_recorder_finished = db.Column(db.Boolean, default=False)
    validator_worker = db.Column(db.Boolean)
    _validator_finished = db.Column(db.Boolean, default=False)

    submit_worker = db.Column(db.Boolean)
    _submit_finished = db.Column(db.Boolean, default=False)
    _submit_functions = db.relationship(
        'SubmitFunction',
        backref='page',
        order_by='SubmitFunction.index',
        collection_class=ordering_list('index')
    )

    _navigator = db.relationship('Navigator', backref='page', uselist=False)
    
    _back = db.Column(db.Boolean)
    back_button = db.Column(MarkupType)
    css = db.Column(MutableListType)
    _direction_from = db.Column(db.String(8))
    _direction_to = db.Column(db.String(8))
    _forward = db.Column(db.Boolean)
    forward_button = db.Column(MarkupType)
    js = db.Column(MutableListType)
    loading_template = db.Column(db.String)
    question_html = db.Column(MarkupType)
    survey_template = db.Column(db.String)
    terminal = db.Column(db.Boolean)
    view_template = db.Column(db.String)
    
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
    
    def __init__(
            self, branch=None, index=None, back_to=None, forward_to=None, 
            nav=None, questions=[], timer_var=None, all_rows=False,
            cache_compile=False, compile_worker=False, compile_functions=[],
            validator_worker=False, submit_worker=False, submit_functions=[], 
            navigator_worker=False, navigator=None, 
            back=None, back_button=None, 
            css=None, forward=True, forward_button=None, 
            js=None, loading_template=None, 
            survey_template=None, terminal=False, view_template=None
            ):        
        self.set_branch(branch, index)
        self.back_to = back_to
        self.forward_to = forward_to
        self.nav = nav or current_app.nav
        self.questions = questions
        self.timer = Question(all_rows=all_rows, data=0, var=timer_var)

        self.cache_compile = cache_compile
        self.compile_worker = compile_worker
        self.compile_functions = (
            compile_functions or current_app.page_compile_functions
        )
        self.validator_worker = validator_worker
        self.submit_worker = submit_worker
        self.submit_functions = (
            submit_functions or current_app.page_submit_functions
        )
        self.navigator_worker = False
        self.navigator = navigator
        
        self.back = back if back is not None else current_app.back
        self.back_button = back_button or current_app.back_button
        self.css = css or current_app.css
        self.forward = forward if forward is not None else current_app.forward
        self.forward_button = forward_button or current_app.forward_button
        self.js = js or current_app.js
        self.loading_template = (
            loading_template or current_app.loading_template
        )
        self.survey_template = survey_template or current_app.survey_template
        self.terminal = terminal
        self.view_template = view_template or current_app.view_template
        super().__init__()

    """API methods"""
    def set_branch(self, branch, index=None):
        self._set_parent(branch, index, 'branch', 'pages')
    
    def clear_responses(self):
        for q in self.questions:
            q.response = None

    def reset_timer(self):
        self.timer.data = 0

    def is_valid(self):
        return all([q.error is None for q in self.questions])
    
    def first_page(self):
        """Indicate that this is the first Page in the experiment"""
        return (
            self.branch is not None and self.branch.is_root 
            and self.index == 0
        )

    """Methods executed during study"""
    def render(self):
        self.start_time = datetime.utcnow()
        html = render_template(self.survey_template, page=self)
        return super().render(html)

    def render_loading(self, method_name):
        """Render loading template

        Send method to task queue, then render loading page.
        """
        db.session.commit()
        current_app.task_queue.enqueue(
            'hemlock.app.tasks.model_method',
            model_class=type(self),
            id=self.id,
            method_name=method_name,
            namespace='/'+self.model_id
        )
        html = render_template(self.loading_template, page=self)
        return super().render(html)

    def compile(self):
        """Compile html
        
        1. Execute compile functions
        2. Compile and join question html
        3. If compile results are cached, remove get worker and functions
        4. Indicate that compile function has completed
        """
        [compile_function() for compile_function in self.compile_functions]
        self.question_html = Markup(''.join(
            [q.compile_html() for q in self.questions]
        ))
        if self.cache_compile:
            self.compile_worker = False
            self.compile_functions.clear()
        self._compile_finished = True

    def record_response(self):
        self._update_timer()
        self._request_method = 'POST'
        self.direction_from = request.form['direction']
        [q.record_response(request.form.getlist(q.model_id)) 
            for q in self.questions]
        self._response_recorder_finished = True
    
    def _update_timer(self):
        if self.start_time is None:
            self.start_time = datetime.utcnow()
        delta = (datetime.utcnow() - self.start_time).total_seconds()
        self.timer.data += delta
    
    def validate(self):
        """Validate responses"""
        if not all ([q.validate() for q in self.questions]):
            self.direction_from = 'invalid'
        self._validator_finished = True
    
    def submit(self):
        """Submit page"""
        [q.record_data() for q in self.questions]
        [submit_function() for submit_function in self.submit_functions]
        self._submit_finished = True
    
    def view_nav(self, indent):
        """Print self and next branch for debugging purposes"""
        HEAD_PART = '<== head page of participant'
        HEAD_BRANCH = '<== head page of branch'
        head_part = HEAD_PART if self == self.part.current_page else ''
        head_branch = HEAD_BRANCH if self == self.branch.current_page else ''
        print(indent, self, head_branch, head_part)
        if self.next_branch in self.part.branch_stack:
            self.next_branch.view_nav()