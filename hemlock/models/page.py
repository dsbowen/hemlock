"""# Page

The survey 'flow' is:

1. **Compile.** Execute a page's `Compile` functions. By default, a page's 
first compile function runs its questions' compile methods in index order.

2. **Render.** Render the page for the participant and wait for them to 
respond.

3. **Record response.** Record the participant's response to every question on
the page. This sets the `response` attribute of the questions.

4. **Validate.** When the participant attempts to submit the page, validate 
the responses. As with the compile method, the validate method executes a 
page's `Validate` functions in index order. By default, a page's first 
validate function runs its questions' validate methods in index order.

5. **Record data.** Record the data associated with the participant's
responses to every question on the page. This sets the `data` attribute of the
questions.

6. **Submit.** Execute the page's `Submit` functions. By default, a page's 
first submit function runs its questions' submit methods in index order.

7. **Navigate.** If the page has a `Navigate` function, create a new branch 
originating from this page.
"""

from ..app import db, settings
from ..tools import Img
from .bases import BranchingBase, HTMLMixin
from .embedded import Timer

from bs4 import BeautifulSoup, Tag
from flask import Markup, current_app, render_template, request
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy_mutable import MutableType

import os
from random import shuffle

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

BANNER = Img(
    src='/hemlock/static/img/hemlock_banner.png',
    alignment='center'
)
BANNER.img['style'] = 'max-width:200px;'

def compile_func(page):
    [q._compile() for q in page.questions]

def validate_func(page):
    [q._validate() for q in page.questions]
    
def submit_func(page):
    [q._submit() for q in page.questions]

def debug_func(driver, page):
    idx = list(range(len(page.questions)))
    shuffle(idx)
    [page.questions[i]._debug(driver) for i in idx]

settings['Page'] = {
    'css': open(os.path.join(DIR_PATH, 'page-css.html'), 'r').read(),
    'js': open(os.path.join(DIR_PATH, 'page-js.html'), 'r').read(),
    'back': False,
    'forward': True,
    'banner': BANNER.render(),
    'terminal': False,
    'compile_functions': compile_func,
    'validate_functions': validate_func,
    'submit_functions': submit_func,
    'debug_functions': debug_func,
}


class Page(HTMLMixin, BranchingBase, db.Model):
    """
    Pages are queued in a branch. A page contains a list of questions which it
    displays to the participant in index order.
    
    It inherits from `hemlock.HTMLMixin`.

    Parameters
    ----------
    branch : hemlock.Branch or None, default=None
        The branch to whose page queue this page belongs.

    template : str, default='page-body.html'
        Template for the page `body`.

    Attributes
    ----------
    back : str or None, default=None
        Text of the back button. If `None`, no back button will appear on the 
        page. You may also set `back` to `True`, which will set the text to 
        `'<<'`.

    banner : str or bs4.Tag, default=hemlock banner
        Banner at the bottom of the page.

    cache_compile : bool, default=False
        Indicates that this page should cache the result of its compile 
        functions. Specifically, it removes all compile functions from the 
        page self `self._compile` is called.

    direction_from : str or None, default=None
        Direction in which the participant navigated from this page. Possible 
        values are `'back'`, `'invalid'`, or `'forward'`.

    direction_to : str or None, default=None
        Direction in which the participant navigated to this page. Possible 
        values are `'back'`, `'invalid'`, and `'forward'`.

    error : str or None, default=None
        Text of the page error message

    forward : str or None, default='>>'
        Text of the forward button. If `None`, no forward button will appear 
        on the page. You may also set `forward` to `True`, which will set the 
        text to `'>>'`.

    g : dict, default={}
        Dictionary of miscellaneous objects.

    index : int or None, default=None
        Order in which this page appears in its branch's page queue.

    terminal : bool, default=False
        Indicates that the survey terminates on this page.

    viewed : bool, default=False
        Indicates that the participant has viewed this page.

    Relationships
    -------------
    part : hemlock.Participant or None, default=None
        Participant to which this page belongs. Read only; derived from `self.
        branch`.

    branch : hemlock.Branch or None, default=None
        Branch to which this page belongs.

    next_branch : hemlock.Branch or None, default=None
        Branch which originated from this page. This is automatically set 
        when this page runs its navigate function.

    back_to : hemlock.Page or None
        Page to which this page navigates when going back. If `None`, this 
        page navigates back to the previous page.

    forward_to : hemlock.Page or None
        Page to which this page navigates when going forward. If `None`, this 
        page navigates to the next page.

    navbar : hemlock.Navbar or None, default=None
        Navigation bar.

    embedded : list of hemlock.Embedded, default=[]
        List of embedded data elements.

    timer : hemlock.Timer
        Tracks timing data for this page.

    questions : list of hemlock.Question, default=[]
        List of questions which this page displays to its participant.

    data_elements : list of hemlock.DataElement
        List of data elements which belong to this page; in order, `self.
        timer`, `self.embedded`, `self.questions`.

    compile_functions : list of hemlock.Compile
        List of compile functions; run before the page is rendered. The 
        default page compile function runs its questions' compile functions 
        in index order.

    compile_worker : hemlock.CompileWorker or None, default=None
        Worker which sends the compile functions to a Redis queue.

    validate_functions : list of hemlock.Validate
        List of validate functions; run to validate participant responses. 
        The default page validate function runs its questions' validate 
        functions in index order.

    validate_worker : hemlock.ValidateWorker or None, default=None
        Worker which sends the validate functions to a Redis queue.

    submit_functions : list of hemlock.Submit
        List of submit functions; run after participant responses have been 
        validated. The default submit function runs its questions' submit 
        functions in index order.

    submit_worker : hemlock.SubmitWorker or None, default=None
        Worker which sends the submit functions to a Redis queue.

    debug_functions : list of hemlock.Debug
        List of debug functions; run during debugging. The default debug 
        function runs its questions' debug functions in *random* order.

    navigate_function : hemlock.Navigate or None, default=None
        Navigate function which returns a new branch originating from this 
        page.

    navigate_worker : hemlock.NavigateWorker
        Worker which sends the navigate function to a Redis queue.
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # relationships
    @property
    def part(self):
        return None if self.branch is None else self.branch.part

    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _branch_head_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

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
    
    # Column attributes
    cache_compile = db.Column(db.Boolean)
    direction_from = db.Column(db.String(8))
    direction_to = db.Column(db.String(8))
    g = db.Column(MutableType)
    index = db.Column(db.Integer)
    terminal = db.Column(db.Boolean)
    viewed = db.Column(db.Boolean, default=False)
    
    def __init__(self, branch=None, template='page-body.html', **kwargs):
        self.branch = branch
        self.timer = Timer()
        super().__init__(template, **kwargs)

    # BeautifulSoup shortcuts
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

    # methods
    def clear_error(self):
        """
        Clear the error message from this page and all of its questions.

        Returns
        -------
        self : hemlock.Page
        """
        self.error = None
        [q.clear_error() for q in self.questions]
        return self
    
    def clear_response(self):
        """
        Clear the response from all of this page's questions.

        Returns
        -------
        self : hemlock.Page
        """
        [q.clear_response() for q in self.questions]
        return self
    
    def first_page(self):
        """
        Returns
        -------
        is_first_page : bool
            Indicator that this is the first page in its participant's survey.
        """
        if self.part is None:
            return False
        for b in self.part.branch_stack:
            if b.pages:
                first_nonempty_branch = b
                break
        return self.branch == first_nonempty_branch and self.index == 0

    def is_valid(self):
        """
        Returns
        -------
        valid : bool
            Indicator that all of the participant's responses are valid. That 
            is, that there are no error messages on the page or any of its 
            questions.
        """
        return not (self.error or any([q.error for q in self.questions]))

    # methods executed during study
    def _compile(self):
        """
        Run the page's compile functions. If `self.cache_compile`, the page's 
        compile functions and compile worker are removed.

        Returns
        -------
        self
        """
        [compile_func(self) for compile_func in self.compile_functions]
        if self.cache_compile:
            self.compile_functions.clear()
            self.compile_worker = None
        return self
    
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
        
        Check validate functions one at a time. If any returns an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        self.error = None
        for validate_func in self.validate_functions:
            error = validate_func(self)
            if error:
                self.error = error
                break
        is_valid = self.is_valid()
        self.direction_form = 'forward' if is_valid else 'invalid'
        return is_valid
    
    def _submit(self):
        [q._record_data() for q in self.questions]
        [submit_func(self) for submit_func in self.submit_functions]

    def _debug(self, driver):
        [debug_func(driver, self) for debug_func in self.debug_functions]
    
    def _view_nav(self, indent):
        """Print self and next branch for debugging purposes"""
        HEAD_PART = '<== head page of participant'
        HEAD_BRANCH = '<== head page of branch'
        head_part = HEAD_PART if self == self.part.current_page else ''
        head_branch = HEAD_BRANCH if self == self.branch.current_page else ''
        print(' '*indent, self, head_branch, head_part)
        if self.next_branch in self.part.branch_stack:
            self.next_branch.view_nav()