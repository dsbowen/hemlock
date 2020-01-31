"""Page database model

`Page`s are nested in `Branch`es. A `Page` contains a list of `Question`s, 
which it displays on the HTML page in `index` order.

The survey 'flow' proceeds as follows:

1. Run the `_compile` method. This method executes a page's `Compile` 
functions. By default, a page's first compile function runs its questions' 
`_compile` methods in `index` order.

2. Render the page.

3. After the participant submits the page, validate the responses. As with 
the `_compile` method, the `_validate` method executes a page's `Validate` 
functions in index order. By default, a page's first validate function runs 
its questions' `_validate` methods in `index` order.

4. Record data and run submit functions. As before, the `_submit` method 
executes the page's `Submit` functions. By default, a page's first submit 
function runs its questions' `_submit` methods in `index` order.

5. If the page has a `Navigate` function, create a new branch originating 
from this page.

A `Page` supplies `data_elements` to its `Branch`. The 'order' of the data 
elements is:
1. A page's timer.
2. A page's embedded data.
3. A page's questions.
"""

from hemlock.app import Settings, db
from hemlock.database.bases import BranchingBase, HTMLMixin
from hemlock.database.data import Timer
from hemlock.tools import Img

from bs4 import BeautifulSoup, Tag
from flask import Markup, current_app, render_template, request
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy_mutable import MutableType

import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

BANNER = Img(
    src='/hemlock/static/img/hemlock_banner.svg',
    alignment='center'
)
BANNER.img['style'] = 'max-width:200px;'

def compile_func(page):
    [q._compile() for q in page.questions]

def validate_func(page):
    [q._validate() for q in page.questions]
    
def submit_func(page):
    [q._submit() for q in page.questions]

@Settings.register('Page')
def page_settings():
    return {
        'css': open(os.path.join(DIR_PATH, 'page-css.html'), 'r').read(),
        'js': open(os.path.join(DIR_PATH, 'page-js.html'), 'r').read(),
        'back': False,
        'forward': True,
        'banner': BANNER.render(),
        'compile_functions': compile_func,
        'validate_functions': validate_func,
        'submit_functions': submit_func,
    }


class Page(HTMLMixin, BranchingBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    """Relationships to primary models"""
    @property
    def part(self):
        return None if self.branch is None else self.branch.part

    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _branch_head_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    g = db.Column(MutableType)
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
        foreign_keys=_back_to_id,
        remote_side=[id]
    )
        
    _forward_to_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    forward_to = db.relationship(
        'Page',
        foreign_keys=_forward_to_id,
        remote_side=[id]
    )
    
    _navbar_id = db.Column(db.Integer, db.ForeignKey('navbar.id'))
    
    embedded = db.relationship(
        'Embedded',
        backref='page',
        order_by='Embedded.index',
        collection_class=ordering_list('index'),
    )

    timer = db.relationship(
        'Timer', 
        uselist=False,
        foreign_keys='Timer._timed_page_id'
    )

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
    name = db.Column(db.String)
    terminal = db.Column(db.Boolean)
    
    @BranchingBase.init('Page')
    def __init__(self, branch=None, **kwargs):
        super().__init__()
        self.timer = Timer()
        self.body = render_template('page-body.html')
        return {'branch': branch, **kwargs}

    """API methods"""
    @property
    def error(self):
        return self.body.text('div.error-msg')

    @error.setter
    def error(self, val):
        self.body.set_element(
            'span.error-msg', val,
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
        return self.body.text('#back-btn')

    @back.setter
    def back(self, val):
        val = '<<' if val is True else val
        self.body.set_element(
            'span.back-btn', val,
            target_selector='#back-btn', 
            gen_target=self._gen_submit,
            args=['back']
        )

    @property
    def forward(self):
        return self.body.text('#forward-btn')

    @forward.setter
    def forward(self, val):
        val = '>>' if val is True else val
        self.body.set_element(
            'span.forward-btn', val,
            target_selector='#forward-btn', 
            gen_target=self._gen_submit,
            args=['forward']
        )

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

    @property
    def banner(self):
        return self.body.select_one('span.banner')
    
    @banner.setter
    def banner(self, val):
        self.body.set_element('span.banner', val)

    def clear_error(self):
        self.error = None
        [q.clear_error() for q in self.questions]
    
    def clear_response(self):
        [q.clear_response() for q in self.questions]
    
    def first_page(self):
        """Indicate that this is the first Page in the survey"""
        if self.part is None:
            return False
        for b in self.part.branch_stack:
            if b.pages:
                first_nonempty_branch = b
                break
        return self.branch == first_nonempty_branch and self.index == 0

    def is_valid(self):
        """Indicates response was valid"""
        return not (self.error or any([q.error for q in self.questions]))

    """Methods executed during study"""
    def _compile(self):
        """Compile html
        
        1. Execute compile functions
        2. If compile results are cached, remove get worker and functions
        """
        [compile_func() for compile_func in self.compile_functions]
        if self.cache_compile:
            self.compile_functions.clear()
            self.compile_worker = None
    
    def _render(self):
        """Render page
        
        This method performs the following functions:
        1. Add page metadata and catch possible submit button errors
        2. Append question HTML
        3. Start the timer
        """
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
        """Add page metadata to soup
        
        Page metadata is its participant's `id` and strongly random `key`. 
        For security, these must match for a participant to access a page.

        Metadata are only necessary for debugging, where a researcher may 
        want to have multiple survey windows open simultaneously. In this 
        case, page metadata are used to associate participants with their 
        pages, rather than Flask-Login's `current_user`.

        To use this functionality, access the URL as {ULR}/?Test=1.
        """
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
        self.error = None
        for validate_func in self.validate_functions:
            error = validate_func()
            if error is not None:
                self.error = error
                break
        is_valid = self.is_valid()
        self.direction_form = 'forward' if is_valid else 'invalid'
        return is_valid
    
    def _submit(self):
        [q._record_data() for q in self.questions]
        [submit_func() for submit_func in self.submit_functions]

    def _debug(self, driver):
        [debug_func(driver) for debug_func in self.debug_functions]
    
    def _view_nav(self, indent):
        """Print self and next branch for debugging purposes"""
        HEAD_PART = '<== head page of participant'
        HEAD_BRANCH = '<== head page of branch'
        head_part = HEAD_PART if self == self.part.current_page else ''
        head_branch = HEAD_BRANCH if self == self.branch.current_page else ''
        print(indent, self, head_branch, head_part)
        if self.next_branch in self.part.branch_stack:
            self.next_branch._view_nav()