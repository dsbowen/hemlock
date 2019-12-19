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
back_btn: html for back button
compiled: indicates that this Page has ever been compiled
css: list of css files
direction_from: direction from which this Page is navigating
direction_to: direction to which this Page was navigated
forward: indicates this Page has a forward button
forward_btn: html for forward button
js: list of js files
template: name of html template
terminal: indicates this Page is the last in the experiment
"""

from hemlock.app import Settings, db
from hemlock.database.private import BranchingBase, HTMLBase
from hemlock.database.html_question import HTMLQuestion
from hemlock.database.types import  MarkupType
from hemlock.tools import CSS, JS

from flask import Markup, current_app, render_template, request, url_for
from sqlalchemy.ext.orderinglist import ordering_list

from random import random, shuffle
from time import sleep


class Page(BranchingBase, HTMLBase, db.Model):
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

    timer = db.relationship(
        'Timer',
        uselist=False,
        foreign_keys='Timer._page_timer_id'
    )

    @property
    def html_questions(self):
        return [q for q in self.questions if isinstance(q, HTMLQuestion)]

    @property
    def questions_with_timer(self):
        return [self.timer]+self.questions if self.timer else self.questions
    
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
    back = db.Column(db.Boolean)
    back_btn = db.Column(MarkupType)
    direction_from = db.Column(db.String(8))
    direction_to = db.Column(db.String(8))
    error = db.Column(db.Text)
    forward = db.Column(db.Boolean)
    forward_btn = db.Column(MarkupType)
    template = db.Column(db.String)
    terminal = db.Column(db.Boolean)

    @property
    def _css(self):
        page_css = super()._css
        question_css = ''.join([q._css for q in self.questions])
        return Markup(page_css + question_css)

    @property
    def _js(self):
        page_js = super()._js
        question_js = ''.join([q._js for q in self.questions])
        return Markup(page_js + question_js)

    @property
    def _error(self):
        """Error in html format"""
        msg = self.error
        return '' if msg is None else Markup(ERROR.format(msg=msg))
    
    @property
    def _back(self):
        return self.back and not self.first_page()
        
    @property
    def _forward(self):
        return self.forward and not self.terminal
    
    def __init__(self, branch=None, **kwargs):
        from hemlock.question_polymorphs import Timer
        self.timer = Timer()
        super().__init__('Page', branch=branch, **kwargs)

    """API methods"""
    def clear_errors(self):
        self.error = None
        [setattr(self, 'error', '') for q in self.questions]
    
    def clear_responses(self):
        [setattr(self, 'response', None) for q in self.questions]
    
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
        2. If compile results are cached, remove get worker and functions
        """
        [compile_func() for compile_func in self.compile_functions]
        if self.cache_compile:
            self.compile_functions.clear()
            self.compile_worker = None
    
    def _render(self):
        """Render page"""
        html = render_template(self.template, page=self)
        if self.timer is not None:
            self.timer.start()
        return self._prettify(html)

    def _record_response(self):
        """Record participant response
        
        Begin by updating the total time. Then get the direction the 
        participant requested for navigation (forward or back). Finally, 
        record the participant's response to each question.
        """
        if self.timer is not None:
            self.timer.pause()
        self.direction_from = request.form.get('direction')
        [
            q._record_response(request.form.getlist(q.model_id)) 
            for q in self.questions
        ]
    
    def _validate(self):
        """Validate response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        for validate_func in self.validate_functions:
            self.error = validate_func()
            if self.error is not None:
                break
        is_valid = self.is_valid()
        self.direction_from = 'forward' if is_valid else 'invalid'
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


ERROR = """
<div class="alert alert-danger w-100" style="text-align:center;">
    {msg}
</div>
"""

STYLESHEETS = [
    CSS(
        url='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
        filename='css/bootstrap-4.4.1.min.css',
        blueprint='hemlock'
    ),
    CSS(
        filename='css/default.css',
        blueprint='hemlock'
    )
]

SCRIPTS = [
    JS(
        url='https://code.jquery.com/jquery-3.4.1.min.js',
        filename='js/jquery-3.4.1.min.js',
        blueprint='hemlock'
    ),
    JS(
        url='https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
        filename='js/popper-1.16.0.min.js',
        blueprint='hemlock'
    ),
    JS(
        url='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js',
        filename='js/bootstrap-4.4.1.min.js',
        blueprint='hemlock'
    ),
    JS(
        filename='js/default.js',
        blueprint='hemlock'
    )
]

BACK_BTN = """
<button id="back-button" name="direction" type="submit" class="btn btn-outline-primary" style="float: left;" value="back"> 
    <<
</button>
"""

FORWARD_BTN = """
<button id="forward-button" name="direction" type="submit" class="btn btn-outline-primary" style="float: right;" value="forward">
    >>
</button>
"""

def compile_func(page):
    [q._compile() for q in page.questions]

def validate_func(page):
    [q._validate() for q in page.questions]
    
def submit_func(page):
    [q._submit() for q in page.questions]

def debug_func(page, driver):
    """Call question debug functions in random order then navigate"""
    order = list(range(len(page.questions)))
    shuffle(order)
    [page.questions[i]._debug(driver) for i in order]
    forward_exists = back_exists = True
    if random() < .8:
        try:
            driver.find_element_by_id('forward-button').click()
        except:
            forward_exists = False
    if random() < .5:
        try:
            driver.find_element_by_id('back-button').click()
        except:
            back_exists = False
    if not (forward_exists or back_exists):
        sleep(3)
    driver.refresh()

@Settings.register('Page')
def page_settings():
    return {
        'css': STYLESHEETS,
        'js': SCRIPTS,
        'back': False,
        'back_btn': BACK_BTN,
        'forward': True,
        'forward_btn': FORWARD_BTN,
        'compile_functions': compile_func,
        'validate_functions': validate_func,
        'submit_functions': submit_func,
        'debug_functions': debug_func,
        'template': 'default.html',
    }