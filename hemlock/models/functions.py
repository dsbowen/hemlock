"""# Function models"""

from ..app import db
from .bases import Base
from .branch import Branch

from sqlalchemy_function import FunctionMixin

import os
from random import random

PARENT_ERR_MSG = """
First argument must be the parent; a Branch, Page, or Question, not {}
"""


class FunctionRegistrar(FunctionMixin, Base):
    """
    Mixin for Function models which provides a method for function 
    registration.
    
    Inherits from 
    [`sqlalchemy_function.FunctionMixin`](<https://dsbowen.github.io/sqlalchemy-function/>).

    Attributes
    ----------
    index : int or None
        Order in which this Function will be executed, relative to other 
        Functions belonging to the same parent object.
    """
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)

    @classmethod
    def register(cls, func):
        """
        This decorator registers a function.

        Parameters
        ----------
        func : callable
            The function to register.
        """
        def add_function(*args, **kwargs):
            if cls != Debug or os.environ.get('DEBUG_FUNCTIONS') != 'False':
                return cls(func, *args, **kwargs)
                
        setattr(cls, func.__name__, add_function)
        return func


class Compile(FunctionRegistrar, db.Model):
    """
    Helps compile a page or question html before it is rendered and displayed 
    to a participant.

    Inherits from `hemlock.FunctionRegistrar`.

    Relationships
    -------------
    page : hemlock.Page or None
        Page to which this model belongs.

    question : hemlock.Question or None
        Question to which this model belongs.

    Examples
    --------
    ```python
    from hemlock import Compile as C, Input, Label, Page, push_app_context

    app = push_app_context()

    @C.register
    def greet(greet_q, name_q):
    \    greet_q.label = '<p>Hello {}!</p>'.format(name_q.response)

    name_q = Input("<p>What's your name?</p>")
    p = Page(Label(compile=C.greet(name_q)))
    name_q.response = 'World'
    p._compile().preview()
    ```
    """
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))


class Debug(FunctionRegistrar, db.Model):
    """
    Run to help debug the survey.

    Inherits from `hemlock.FunctionRegistrar`.

    Attributes
    ----------
    p_exec : float, default=1.
        Probability that the debug function will execute. You can set this by
        passing in an `p_exec` keyword argument to the constructor.

    Relationships
    -------------
    page : hemlock.Page or None
        Page to which this model belongs.

    question : hemlock.Question or None
        Question to which this model belongs.

    Examples
    --------
    ```python
    from hemlock import Debug as D, Input, Page, push_app_context
    from hemlock.tools import chromedriver

    app = push_app_context()

    driver = chromedriver()

    @D.register
    def greet(driver, greet_q):
    \    inpt = greet_q.input_from_driver(driver)
    \    inpt.clear()
    \    inpt.send_keys('Hello World!')

    p = Page(Input('<p>Enter a greeting.</p>', debug=D.greet()))
    p.debug.pop(-1) # so the page won't navigate
    p.preview(driver)._debug(driver)
    ```
    """
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    p_exec = db.Column(db.Float)

    def __init__(self, *args, **kwargs):
        self.p_exec = kwargs.pop('p_exec', 1.)
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Execute the debug function with probability `self.p_exec`.
        """
        if random() < self.p_exec:
            return super().__call__(*args, **kwargs)


class Validate(FunctionRegistrar, db.Model):
    """
    Validates a participant's response.

    Inherits from `hemlock.FunctionRegistrar`.

    Attributes
    ----------
    error_msg : str or None
        If the validate function returns an error message, the `error_msg`
        attribute is returned instead of the output of the validate function.
        You can set this by passing in an `error_msg` keyword argument to the
        constructor.

    Relationships
    -------------
    page : hemlock.Page or None
        Page to which this model belongs.

    question : hemlock.Question or None
        Question to which this model belongs.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    @Validate.register
    def match(inpt, pattern):
    \    if inpt.response != pattern:
    \        return '<p>You entered "{}", not "{}"</p>'.format(inpt.response, pattern)

    pattern = 'hello world'
    inpt = Input(validate=V.match(pattern))
    inpt.response = 'goodbye moon'
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    You entered "goodbye moon", not "hello world"
    ```
    """
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    error_msg = db.Column(db.Text)

    def __init__(self, *args, **kwargs):
        self.error_msg = kwargs.pop('error_msg', None)
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Returns
        -------
        error_msg : str or None
            Return `None` if there is no error. If there is an error, return
            `self.error_msg` or the output of `self.func`.
        """
        error_msg = super().__call__(*args, **kwargs)
        if error_msg:
            return self.error_msg or error_msg

            
class Submit(FunctionRegistrar, db.Model):
    """
    Runs after a participant has successfully submitted a page.

    Inherits from `hemlock.FunctionRegistrar`.

    Relationships
    -------------
    page : hemlock.Page or None
        Page to which this model belongs.

    question : hemlock.Question or None
        Question to which this model belongs.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    @S.register
    def get_initials(name_q):
    \    names = name_q.response.split()
    \    name_q.data = '.'.join([name[0] for name in names]) + '.'

    inpt = Input("<p>What's your name?</p>", submit=S.get_initials())
    inpt.response = 'Andrew Yang'
    inpt._submit().data
    ```

    Out:

    ```
    A.Y.
    ```
    """
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))


class Navigate(FunctionRegistrar, db.Model):
    """
    Creates a new branch to which the participant will navigate.

    Relationships
    -------------
    branch : hemlock.Branch or None
        Branch to which this model belongs.

    page : hemlock.Page or None
        Page to which this model belongs.

    Examples
    --------
    ```python
    from hemlock import Branch, Navigate as N, Page, Participant, push_app_context

    def start():
    \    return Branch(Page(), navigate=N.end())

    @N.register
    def end(start_branch):
    \    return Branch(Page(terminal=True))

    app = push_app_context()

    part = Participant.gen_test_participant(start)
    part.view_nav()
    ```

    Out:

    ```
    <Branch 1>
    <Page 1> C 

    C = current page 
    T = terminal page
    ```

    In:

    ```python
    part.forward().view_nav()
    ```

    Out:

    ```
    <Branch 1>
    <Page 1>  
    \    <Branch 2>
    \    <Page 2> C T

    C = current page 
    T = terminal page
    ```
    """
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    def __call__(self, *args, **kwargs):
        """
        Create a new branch and 'link' it to the tree. Linking in the new 
        branch involves setting the `next_branch` and `origin_branch` or 
        `origin_page` relationships.
        """
        next_branch = super().__call__(*args, **kwargs)
        assert isinstance(next_branch, Branch)
        parent = self.branch or self.page
        if parent is not None:
            self._set_relationships(parent, next_branch)
        next_branch.current_page = next_branch.start_page
        return next_branch

    def _set_relationships(self, parent, next_branch):
        """Set relationships between next_branch and its origin"""
        parent.next_branch = next_branch
        if isinstance(parent, Branch):
            next_branch.origin_page = None
            next_branch.origin_branch = parent
        else:
            # origin is hemlock.Page
            next_branch.origin_branch = None
            next_branch.origin_page = parent