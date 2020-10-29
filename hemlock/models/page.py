"""# Page

The survey 'flow' is:

1. **Compile.** Execute a page's compile functions. By default, a page's 
first compile function runs its questions' compile methods in index order.

2. **Render.** Render the page for the participant and wait for them to 
respond.

3. **Record response.** Record the participant's response to every question on
the page. This sets the `response` attribute of the questions.

4. **Validate.** When the participant attempts to submit the page, validate 
the responses. As with the compile method, the validate method executes a 
page's validate functions in index order. By default, a page's first 
validate function runs its questions' validate methods in index order.

5. **Record data.** Record the data associated with the participant's
responses to every question on the page. This sets the `data` attribute of the
questions.

6. **Submit.** Execute the page's submit functions. By default, a page's 
first submit function runs its questions' submit methods in index order.

7. **Navigate.** If the page has a navigate function, create a new branch 
originating from this page.
"""

from ..app import db, settings
from ..tools import img
from .bases import BranchingBase
from .embedded import Timer
from .worker import Worker
from .functions import Compile, Validate, Submit, Debug

from bs4 import BeautifulSoup
from flask import current_app, render_template, request
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy_mutable import (
    HTMLAttrsType, MutableType, MutableListType, MutableListJSONType
)

import os
import webbrowser
from random import random, shuffle
from tempfile import NamedTemporaryFile
from time import sleep

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

@Compile.register
def compile_questions(page):
    """
    Execute the page's questions' compile methods in index order.

    Parameters
    ----------
    page : hemlock.Page
    """
    [q._compile() for q in page.questions]

@Validate.register
def validate_questions(page):
    """
    Execute the page's questions' validate methods in index order.

    Parameters
    ----------
    page : hemlock.Page
    """
    [q._validate() for q in page.questions]
    
@Submit.register
def submit_questions(page):
    """
    Execute the page's questions' submit methods in index order.

    Parameters
    ----------
    page : hemlock.Page
    """
    [q._submit() for q in page.questions]

@Debug.register
def debug_questions(driver, page):
    """
    Execute the page's questions' debug methods in  *random* order.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    page : hemlock.Page
    """
    order = list(range(len(page.questions)))
    shuffle(order)
    [page.questions[i]._debug(driver) for i in order]

@Debug.register
def navigate(driver, page, p_forward=.8, p_back=.1, sleep_time=3):
    """
    Randomly navigate forward or backward, or refresh the page. By default, it
    is executed after the default page debug function.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    page : hemlock.Page

    p_forward : float, default=.8
        Probability of clicking the forward button.

    p_back : float, default=.1
        Probability of clicking the back button.

    sleep_time : float, default=3
        Number of seconds to sleep if there is no forward or back button on
        the page.

    Notes
    -----
    The probability of refreshing the page is `1-p_forward-p_back`.
    """
    forward_exists = back_exists = True
    if random() < p_forward:
        try:
            return driver.find_element_by_id('forward-btn').click()
        except:
            forward_exists = False
    if random() < p_back / (1 - p_forward):
        try:
            return driver.find_element_by_id('back-btn').click()
        except:
            back_exists = False
    if not (forward_exists or back_exists):
        sleep(sleep_time)
        navigate(driver, page, p_forward, p_back, sleep_time)
    driver.refresh()

settings['Page'] = dict(
    timer=None,
    template='hemlock/page.html',
    css=open(os.path.join(DIR_PATH, 'page-css.html'), 'r').read() \
        .splitlines(),
    js=open(os.path.join(DIR_PATH, 'page-js.html'), 'r').read() \
        .splitlines(),
    error_attrs={
        'class': ['alert', 'alert-danger', 'w-100', 'error'],
        'style': {'text-align': 'center'}
    },
    back=False,
    back_btn_attrs={
        'id': 'back-btn',
        'class': ['btn', 'btn-primary'],
        'name': 'direction',
        'type': 'submit',
        'style': {'float': 'left'},
        'value': 'back'
    },
    forward=True,
    forward_btn_attrs={
        'id': 'forward-btn',
        'class': ['btn', 'btn-primary'],
        'name': 'direction',
        'type': 'submit',
        'style': {'float': 'right'},
        'value': 'forward'
    },
    banner=img(
        '/hemlock/static/img/hemlock_banner.png',
        img_align='center', 
        img_attrs={'style': 'max-width:200px;', 'alt': 'Hemlock banner'}
    ),
    compile=[compile_questions],
    validate=[validate_questions],
    submit=[submit_questions],
    debug=[debug_questions, navigate],
    cache_compile=False,
    terminal=False,
)


class Page(BranchingBase, db.Model):
    """
    Pages are queued in a branch. A page contains a list of questions which it
    displays to the participant in index order.
    
    It inherits from [`hemlock.model.HTMLMixin`](bases.md).

    Parameters
    ----------
    \*questions : list of hemlock.Question, default=[]
        Questions to be displayed on this page.

    template : str, default='hemlock/page-body.html'
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
        functions. Specifically, it removes all compile functions and the 
        compile worker from the page self `self._compile` is called.

    direction_from : str or None, default=None
        Direction in which the participant navigated from this page. Possible 
        values are `'back'`, `'invalid'`, or `'forward'`.

    direction_to : str or None, default=None
        Direction in which the participant navigated to this page. Possible 
        values are `'back'`, `'invalid'`, and `'forward'`.

    error : str or None, default=None
        Text of the page error message.

    forward : str or None, default='>>'
        Text of the forward button. If `None`, no forward button will appear 
        on the page. You may also set `forward` to `True`, which will set the 
        text to `'>>'`.

    g : dict, default={}
        Dictionary of miscellaneous objects.

    index : int or None, default=None
        Order in which this page appears in its branch's page queue.

    navbar : sqlalchemy_mutablesoup.MutableSoupType
        Navigation bar.

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

    embedded : list of hemlock.Embedded, default=[]
        List of embedded data elements.

    timer : hemlock.Timer or None, default=hemlock.Timer
        Tracks timing data for this page.
        1. Timer can be set as a `Timer` object.
        2. Setting `timer` to a `str` or `None` sets the timer object 
        variable.
        3. Setting `timer` to a `tuple` sets the timer object variable and 
        data rows.
        4. Setting `timer` to a `dict` sets the timer object attributes. The
        `dict` maps attribute names to values.

    questions : list of hemlock.Question, default=[]
        List of questions which this page displays to its participant.

    data_elements : list of hemlock.DataElement
        List of data elements which belong to this page; in order, `self.
        timer`, `self.embedded`, `self.questions`.

    compile : list of hemlock.Compile
        List of compile functions; run before the page is rendered. The 
        default page compile function runs its questions' compile functions 
        in index order.

    compile_worker : hemlock.Worker or None, default=None
        Worker which sends the compile functions to a Redis queue.

    validate : list of hemlock.Validate
        List of validate functions; run to validate participant responses. 
        The default page validate function runs its questions' validate 
        functions in index order.

    validate_worker : hemlock.Worker or None, default=None
        Worker which sends the validate functions to a Redis queue.

    submit : list of hemlock.Submit
        List of submit functions; run after participant responses have been 
        validated. The default submit function runs its questions' submit 
        functions in index order.

    submit_worker : hemlock.Worker or None, default=None
        Worker which sends the submit functions to a Redis queue.

    navigate : hemlock.Navigate or None, default=None
        Navigate function which returns a new branch originating from this 
        page.

    navigate_worker : hemlock.Worker
        Worker which sends the navigate function to a Redis queue.

    debug_functions : list of hemlock.Debug
        List of debug functions; run during debugging. The default debug 
        function runs its questions' debug functions in *random* order.

    Examples
    --------
    ```python
    from hemlock import Page, push_app_context

    app = push_app_context()

    Page(Label('<p>Hello World</p>')).preview()
    ```
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
        'Page', foreign_keys=_back_to_id, remote_side=[id]
    )
        
    _forward_to_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    forward_to = db.relationship(
        'Page', foreign_keys=_forward_to_id, remote_side=[id]
    )
    
    embedded = db.relationship(
        'Embedded',
        backref='page',
        order_by='Embedded.index',
        collection_class=ordering_list('index'),
    )

    _timer = db.relationship(
        'Timer', uselist=False, foreign_keys='Timer._timed_page_id'
    )

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, val):
        if isinstance(val, Timer):
            self._timer = val
            return
        if self._timer is None:
            self._timer = Timer()
        if isinstance(val, str) or val is None:
            self._timer.var = val
        elif isinstance(val, tuple):
            self._timer.var, self._timer.data_rows = val
        elif isinstance(val, dict):
            [setattr(self._timer, key, value) for key, value in val.items()]
        else:
            raise ValueError('Invalid value {} for timer'.format(val))        

    questions = db.relationship(
        'Question', 
        backref='page',
        order_by='Question.index',
        collection_class=ordering_list('index')
    )

    @property
    def data_elements(self):
        timer = [self.timer] if self.timer else []
        return self.embedded + timer + self.questions

    compile_worker = db.relationship(
        'Worker', uselist=False, foreign_keys='Worker._compile_id'
    )
    validate_worker = db.relationship(
        'Worker', uselist=False, foreign_keys='Worker._validate_id'
    )
    submit_worker = db.relationship(
        'Worker', uselist=False, foreign_keys='Worker._submit_id'
    )
    navigate_worker = db.relationship(
        'Worker', uselist=False, foreign_keys='Worker._navigate_page_id'
    )

    @validates(
        'compile_worker',
        'hello_world_worker', 
        'validate_worker', 
        'submit_worker', 
        'navigate_worker'
    )
    def set_worker(self, key, worker):
        if not worker:
            return
        return worker if isinstance(worker, Worker) else Worker()

    # HTML attibutes
    template = db.Column(db.String)
    css = db.Column(MutableListJSONType)
    js = db.Column(MutableListJSONType)
    navbar = db.Column(db.Text)
    error = db.Column(db.Text)
    error_attrs = db.Column(HTMLAttrsType)
    forward = db.Column(db.String)
    forward_btn_attrs = db.Column(HTMLAttrsType)
    back = db.Column(db.String)
    back_btn_attrs = db.Column(HTMLAttrsType)
    banner = db.Column(db.Text)

    @validates('forward', 'back')
    def validate_direction(self, key, val):
        if not val:
            return None
        if val is True:
            return '&gt;&gt;' if key == 'forward' else '&lt;&lt;'
        return val

    # Function columns
    compile = db.Column(MutableListType)
    debug = db.Column(MutableListType)
    validate = db.Column(MutableListType)
    submit = db.Column(MutableListType)

    # Additional attributes
    cache_compile = db.Column(db.Boolean)
    direction_from = db.Column(db.String(8))
    direction_to = db.Column(db.String(8))
    g = db.Column(MutableType)
    index = db.Column(db.Integer)
    name = db.Column(db.String)
    terminal = db.Column(db.Boolean)
    viewed = db.Column(db.Boolean, default=False)

    def __init__(self, *questions, extra_css=[], extra_js=[], **kwargs):
        def add_extra(attr, extra):
            # add extra css or javascript
            if extra:
                assert isinstance(extra, (str, list))
                if isinstance(extra, str):
                    attr.append(extra)
                else:
                    attr += extra

        self.questions = list(questions)
        super().__init__(**kwargs)
        add_extra(self.css, extra_css)
        add_extra(self.js, extra_js)

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
        if self.branch is None or self.index > 0:
            return False
        for branch in self.part.branch_stack:
            if branch.pages:
                first_nonempty_branch = branch
                break
        return self.branch == first_nonempty_branch

    def last_page(self):
        """
        Returns
        -------
        is_last_page : bool
            Indicator that this is the last page in its participant's survey.

        Notes
        -----
        This method assumes that if this page or its branch have a navigate
        function or next branch that this page is not the last (i.e. that the
        next branch will have pages). Avoid relying on this method if e.g. 
        this page's navigate function may return an empty branch.
        """
        if (
            self.branch is None 
            # not last page on the branch
            or self.index < len(self.branch.pages) - 1
            or self.navigate is not None
            or self.next_branch is not None
            or self.branch.navigate is not None
            or self.branch.next_branch is not None
        ):
            return False
        for branch in self.part.branch_stack:
            if self.branch == branch:
                return True
            if (
                branch.current_page is not None 
                and branch.current_page.last_page()
            ):
                return False

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

    def preview(self, driver=None):
        """
        Preview the page in a browser window.

        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver or None, default=None
            Driver to preview page debugging. If `None`, the page will be
            opened in a web browser.

        Returns
        -------
        self : hemlock.Page

        Notes
        -----
        If running in WSL, first specify the distribution as an environment
        variable. For example, if running in Ubuntu:

        ```bash
        $ export WSL_DISTRIBUTION=Ubuntu
        ```

        This method does not run the compile functions.
        """
        def get_static_paths():
            # get a list of (static_url_path, static_folder tuples)
            paths = [(current_app.static_url_path, current_app.static_folder)]
            paths += [
                (bp.static_url_path, bp.static_folder)
                for bp in current_app.blueprints.values()
            ]
            return [path for path in paths if path[0]]

        def convert_rel_paths(attr):
            # convert relative paths to absolute paths
            elements = html.select('[{0}]:not([{0}=""])'.format(attr))
            [convert_rel_path(e, attr) for e in elements]

        def convert_rel_path(element, attr):
            # convert relative path for a single tag (element)
            url = element.attrs.get(attr)
            for path, folder in static_paths:
                if url.startswith(path):
                    element[attr] = dist + folder + url[len(path):]
                    break

        def create_tmp_file():
            # create tempoarary file and write out HTML
            with NamedTemporaryFile('w', suffix='.html', delete=False) as f:
                f.write(str(html))
                uri = 'file://'+('wsl$'+ dist + f.name if dist else f.name)
                if hasattr(current_app, 'tmpfiles'):
                    current_app.tmpfiles.append(f.name)
            return uri

        dist = os.environ.get('WSL_DISTRIBUTION')
        if not dist.startswith('/'):
            dist = '/'+dist
        static_paths = get_static_paths()
        html = BeautifulSoup(self._render(), 'lxml')
        convert_rel_paths('href')
        convert_rel_paths('src')
        uri = create_tmp_file()
        if driver is None:
            webbrowser.open(uri)
        else:
            driver.get(uri)
        return self

    def view_nav(self, indent=0):
        """
        Print the navigation starting at this page for debugging purposes.
        
        Parameters
        ----------
        indent : int, default=0
            Starting indentation.

        Returns
        -------
        self : hemlock.Page
        """
        # Note to self: the commented lines were very useful for me when 
        # debugging the navigation system; less so for users

        # HEAD_PART = '<== head page of participant'
        # HEAD_BRANCH = '<== head page of branch'
        HEAD_PART = 'C '
        head_part = HEAD_PART if self == self.part.current_page else ''
        # head_branch = HEAD_BRANCH if self == self.branch.current_page else ''
        # print(' '*indent, self, head_branch, head_part)
        terminal = 'T' if self.terminal else ''
        print(' '*indent, self, head_part+terminal)
        if self.next_branch in self.part.branch_stack:
            self.next_branch.view_nav()
        return self

    # methods executed during study
    def _compile(self):
        """
        Run the page's compile functions. If `self.cache_compile`, the page's 
        compile functions and compile worker are removed.

        Returns
        -------
        self
        """
        # the page uses its compile functions to f itself
        [f(self) for f in self.compile]
        if self.cache_compile:
            self.compile = self.compile_worker = None
        return self
    
    def _render(self):
        return render_template(self.template, page=self)

    def _record_response(self):
        """Record participant response
        
        Begin by updating the total time. Then get the direction the 
        participant requested for navigation (forward or back). Finally, 
        record the participant's response to each question.
        """
        self.direction_from = request.form.get('direction')
        [q._record_response() for q in self.questions]
        return self
    
    def _validate(self):
        """Validate response
        
        Check validate functions one at a time. If any returns an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        self.clear_error()
        for f in self.validate:
            self.error = f(self)
            if self.error:
                break
        is_valid = self.is_valid()
        self.direction_from = 'forward' if is_valid else 'invalid'
        return is_valid
    
    def _submit(self):
        [q._record_data() for q in self.questions]
        [f(self) for f in self.submit]
        return self

    def _debug(self, driver):
        [f(driver, self) for f in self.debug]
        return self