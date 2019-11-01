"""Page database model

Relationships to primary models:

branch: Branch to which this Page belongs
next_branch: Branch to which this Page navigates
back_to: Page to which this Page navigates on 'back'
forward_to: Page to which this Page navigates on 'forward'
nav: Navigation bar
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
"""

from hemlock.app import db
from hemlock.database.private import BranchingBase, CompileBase, FunctionBase
from hemlock.database.types import  MarkupType
from hemlock.tools.static import render_css, render_js

from datetime import datetime
from flask import Markup, current_app, render_template, request, url_for
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import MutableListType, MutableDictType

DIRECTIONS = ['back', 'forward', 'invalid', None]


class Page(BranchingBase, CompileBase, FunctionBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    """Relationships to primary models"""
    @property
    def part(self):
        return None if self.branch is None else self.branch.part

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
    total_time = db.Column(db.Integer, default=0)
    timer = db.relationship(
        'Question', # Update to 'Timer'
        uselist=False,
        foreign_keys='Question._page_timer_id'
    )

    @property
    def questions_with_timer(self):
        if self.timer is None:
            return self.questions
        return [self.timer]+self.questions
    
    """Relationships to function models and workers"""
    cache_compile = db.Column(db.Boolean)
    compile_functions = db.relationship(
        'Compile',
        backref='page',
        order_by='Compile.index',
        collection_class=ordering_list('index')
    )
    compile_worker = db.relationship(
        'CompileWorker', 
        backref='page', 
        uselist=False
    )

    validate_functions = db.relationship(
        'Validate',
        backref='page',
        order_by='Validate.index',
        collection_class=ordering_list('index')
    )
    validate_worker = db.relationship(
        'ValidateWorker',
        backref='page',
        uselist=False
    )

    submit_functions = db.relationship(
        'Submit',
        backref='page',
        order_by='Submit.index',
        collection_class=ordering_list('index')
    )
    submit_worker = db.relationship(
        'SubmitWorker',
        backref='page',
        uselist=False
    )

    navigate_function = db.relationship(
        'Navigate', 
        backref='page', 
        uselist=False
    )
    navigate_worker = db.relationship(
        'NavigateWorker',
        backref='page', 
        uselist=False
    )
    
    """Columns"""
    _back = db.Column(db.Boolean)
    back_button = db.Column(MarkupType)
    css = db.Column(MutableListType)
    _direction_from = db.Column(db.String(8))
    _direction_to = db.Column(db.String(8))
    error = db.Column(db.Text)
    _forward = db.Column(db.Boolean)
    forward_button = db.Column(MarkupType)
    js = db.Column(MutableListType)
    _nav_html = db.Column(MarkupType)
    _question_html = db.Column(MarkupType)
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
            nav=None, questions=[], timer=None,
            cache_compile=False, compile_functions=[], compile_worker=None,
            validate_functions=[], validate_worker=None,
            submit_functions=[], submit_worker=None,
            navigate_function=None, navigate_worker=None,
            back=None, back_button=None, css=None, 
            forward=True, forward_button=None, js=None,
            survey_template=None, terminal=False, view_template=None
        ):        
        self.set_branch(branch, index)
        self.back_to = back_to
        self.forward_to = forward_to
        self.nav = nav
        self.questions = questions
        self.timer = timer
        
        self._set_function_relationships()
        self.cache_compile = cache_compile
        self.compile_functions = compile_functions
        self.compile_worker = compile_worker
        self.validate_functions = validate_functions
        self.validate_worker = validate_worker
        self.submit_functions = submit_functions
        self.submit_worker = submit_worker
        self.navigate_function = navigate_function
        self.navigate_worker = navigate_worker
        
        self.back = back
        self.back_button = back_button
        self.css = css
        self.forward = forward
        self.forward_button = forward_button
        self.js = js
        self.survey_template = survey_template
        self.terminal = terminal
        self.view_template = view_template
        
        super().__init__(current_app.page_settings)

    """API methods"""
    def set_branch(self, branch, index=None):
        self._set_parent(branch, index, 'branch', 'pages')
    
    def clear_responses(self):
        """Clear all question responses"""
        for q in self.questions:
            q.response = None
    
    def first_page(self):
        """Indicate that this is the first Page in the experiment"""
        return (
            self.branch is not None and self.branch.is_root 
            and self.index == 0
        )

    def is_valid(self):
        """Indicates response was valid"""
        return (
            self.error is None 
            and all([q.error is None for q in self.questions])
        )

    """Methods executed during study"""
    def _compile(self):
        """Compile html
        
        1. Execute compile functions
        2. Compile message and question html
        3. If compile results are cached, remove get worker and functions
        """
        [compile_function() for compile_function in self.compile_functions]
        self._nav_html = self.nav.render() if self.nav is not None else ''
        self._question_html = Markup(''.join(
            [q._compile() for q in self.questions]
        ))
        if self.cache_compile:
            self.compile_functions.clear()
            self.compile_worker = None
    
    def _render(self):
        """Render page"""
        self.start_time = datetime.utcnow()
        html = render_template(self.survey_template, page=self)
        return super()._render(html)

    @property
    def _css(self):
        return render_css(self)

    @property
    def _js(self):
        return render_js(self)

    def _record_response(self):
        """Record participant response
        
        Begin by updating the total time. Then get the direction the 
        participant requested for navigation (forward or back). Finally, 
        record the participant's response to each question.
        """
        if self.start_time is None:
            self.start_time = datetime.utcnow()
        delta = (datetime.utcnow() - self.start_time).total_seconds()
        self.total_time += int(delta)
        self.direction_from = request.form['direction']
        [q._record_response(request.form.getlist(q.model_id)) 
            for q in self.questions]
    
    def _validate(self):
        """Validate response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        valid = True
        for validate_function in self.validate_functions:
            self.error = validate_function()
            if self.error is not None:
                self.direction_from = 'invalid'
                valid = False
                break
        return valid
    
    def _submit(self):
        """Submit page
        
        Record data (submit) for each question, then run submit functions.
        """
        [q._submit() for q in self.questions]
        [submit_function() for submit_function in self.submit_functions]
    
    def _view_nav(self, indent):
        """Print self and next branch for debugging purposes"""
        HEAD_PART = '<== head page of participant'
        HEAD_BRANCH = '<== head page of branch'
        head_part = HEAD_PART if self == self.part.current_page else ''
        head_branch = HEAD_BRANCH if self == self.branch.current_page else ''
        print(indent, self, head_branch, head_part)
        if self.next_branch in self.part.branch_stack:
            self.next_branch._view_nav()