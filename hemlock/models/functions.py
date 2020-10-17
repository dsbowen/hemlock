"""# Function column types"""

from sqlalchemy_mutable import Mutable, partial

from random import random


class Base():
    @property
    def __name__(self):
        return self.func.__name__

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @classmethod
    def register(cls, func):
        def add_function(*args, **kwargs):
            return partial(cls(func), *args, **kwargs)

        setattr(cls, func.__name__, add_function)
        return func


class Compile(Base):
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


class Debug(Base):
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
    def __call__(self, *args, **kwargs):
        p_exec = kwargs.pop('p_exec', 1)
        if random() < p_exec:
            return self.func(*args, **kwargs)


class Validate(Base):
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

    @V.register
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
    def __call__(self, *args, **kwargs):
        custom_error_msg = kwargs.pop('error_msg', None)
        error_msg = self.func(*args, **kwargs)
        if error_msg:
            return custom_error_msg or error_msg

            
class Submit(Base):
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


class Navigate(Base):
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