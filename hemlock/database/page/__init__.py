"""Page database model"""

from hemlock.app import db
from hemlock.database.bases import BranchingBase, HTMLMixin
from hemlock.database.types import MutableSoupType
from hemlock.database.page.navbar import *
import hemlock.database.page.settings

from bs4 import BeautifulSoup, Tag
from flask import Markup, current_app, render_template, request
from sqlalchemy.ext.orderinglist import ordering_list


class Page(HTMLMixin, BranchingBase, db.Model):
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
    
    embedded = db.relationship(
        'Embedded',
        backref='page',
        order_by='Embedded.index',
        collection_class=ordering_list('index'),
        foreign_keys='Embedded._page_id'
    )

    timer = db.relationship('Timer', uselist=False)

    questions = db.relationship(
        'Question', 
        backref='page',
        order_by='Question.index',
        collection_class=ordering_list('index')
    )

    @property
    def data_elements(self):
        timer = [self.timer] if self.timer else []
        return timer + self.embedded + self.questions
    
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

    debug_functions = db.relationship(
        'Debug',
        backref='page',
        order_by='Debug.index',
        collection_class=ordering_list('index')
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
    direction_from = db.Column(db.String(8))
    direction_to = db.Column(db.String(8))
    terminal = db.Column(db.Boolean)
    
    @BranchingBase.init('Page')
    def __init__(self, branch=None, **kwargs):
        super().__init__()
        from hemlock.database import Timer
        self.timer = Timer()
        self.body = render_template('page-body.html')
        return {'branch': branch, **kwargs}

    """API methods"""
    @property
    def error(self):
        return self.text('div.error-msg')

    @error.setter
    def error(self, val):
        self._set_element(
            val, 
            parent_selector='span.error-msg', 
            target_selector='div.error-msg', 
            gen_target=self._gen_error
        )

    def _gen_error(self):
        """Generate error tag"""
        err = Tag(name='div')
        err['class'] = 'error-msg alert alert-danger w=100'
        err['style'] = 'text-align: center;'
        return err

    @property
    def back(self):
        return self.text('#back-btn')

    @back.setter
    def back(self, val):
        val = '<<' if val is True else val
        self._set_element(
            val, 
            parent_selector='span.back-btn', 
            target_selector='#back-btn', 
            gen_target=self._gen_back
        )
    
    def _gen_back(self):
        """Generate back button Tag"""
        return self._gen_submit('back')

    @property
    def forward(self):
        return self.text('#forward-btn')

    @forward.setter
    def forward(self, val):
        val = '>>' if val is True else val
        self._set_element(
            val, 
            parent_selector='span.forward-btn', 
            target_selector='#forward-btn', 
            gen_target=self._gen_forward
        )

    def _gen_forward(self):
        """Generate forward button"""
        return self._gen_submit('forward')

    def _gen_submit(self, direction):
        """Generate submit (back or forward) button"""
        btn = Tag(name='button')
        btn['id'] = direction+'-btn'
        btn['name'] = 'direction'
        btn['type'] = 'submit'
        btn['class'] = 'btn btn-outline-primary'
        float_ = 'left' if direction == 'back' else 'right'
        btn['style'] = 'float: {};'.format(float_)
        btn['value'] = direction
        return btn

    def clear_errors(self):
        self.error = None
        [setattr(self, 'error', None) for q in self.questions]
    
    def clear_responses(self):
        [setattr(self, 'response', None) for q in self.questions]
    
    def first_page(self):
        """Indicate that this is the first Page in the survey"""
        return (
            self.branch is not None and self.branch.is_root 
            and self.index == 0
        )

    def is_valid(self):
        """Indicates response was valid"""
        return not (self.error or any([q.error for q in self.questions]))

    """Methods executed during study"""
    def _compile(self):
        """Compile html
        
        1. Execute compile functions
        2. If compile results are cached, remove get worker and functions
        """
        [compile_fn() for compile_fn in self.compile_functions]
        if self.cache_compile:
            self.compile_functions.clear()
            self.compile_worker = None
    
    def _render(self):
        """Render page"""
        html = render_template('page.html', page=self)
        soup = BeautifulSoup(html, 'html.parser')
        self._add_page_metadata(soup)
        self._catch_btns(soup)
        question_html = soup.select_one('span.question-html')
        [question_html.append(q._render()) for q in self.questions]
        if self.timer is not None:
            self.timer.start()
        return str(soup)
    
    def _add_page_metadata(self, soup):
        """Add page metadata to soup"""
        meta_html = render_template('page-meta.html', page=self)
        meta_soup = BeautifulSoup(meta_html, 'html.parser')
        form = soup.select_one('form')
        if form is not None:
            form.insert(0, meta_soup)
    
    def _catch_btns(self, soup):
        """Catch submit button errors

        Back button should not be present on the first page of the survey.
        Forward button should not be present on the terminal page.
        """
        if self.first_page():
            back_btn = soup.select_one('span.back-btn')
            if back_btn is not None:
                back_btn.clear()
        if self.terminal:
            forward_btn = soup.select_one('span.forward-btn')
            if forward_btn is not None:
                forward_btn.clear()

    def _record_response(self):
        """Record participant response
        
        Begin by updating the total time. Then get the direction the 
        participant requested for navigation (forward or back). Finally, 
        record the participant's response to each question.
        """
        if self.timer is not None:
            self.timer.pause()
        self.direction_from = request.form.get('direction')
        [q._record_response() for q in self.questions]
    
    def _validate(self):
        """Validate response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        for validate_fn in self.validate_functions:
            self.error = validate_fn()
            if self.error is not None:
                break
        is_valid = self.is_valid()
        self.direction_from = 'forward' if is_valid else 'invalid'
        return is_valid
    
    def _submit(self):
        [q._record_data() for q in self.questions]
        [submit_fn() for submit_fn in self.submit_functions]

    def _debug(self, driver):
        [debug_fn(driver) for debug_fn in self.debug_functions]
    
    def _view_nav(self, indent):
        """Print self and next branch for debugging purposes"""
        HEAD_PART = '<== head page of participant'
        HEAD_BRANCH = '<== head page of branch'
        head_part = HEAD_PART if self == self.part.current_page else ''
        head_branch = HEAD_BRANCH if self == self.branch.current_page else ''
        print(indent, self, head_branch, head_part)
        if self.next_branch in self.part.branch_stack:
            self.next_branch._view_nav()