"""# Function column types

All of these classes inherit from 
[`sqlalchemy_mutable.partial`](https://dsbowen.github.io/sqlalchemy-mutable).
"""

from sqlalchemy_mutable import partial

from random import random


class Compile(partial):
    """
    Helps compile a page or question html before it is rendered and displayed 
    to a participant.

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


class Debug(partial):
    """
    Run to help debug the survey.

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
    def __init__(self, func, *args, p_exec=1., **kwargs):
        super().__init__(func, *args, **kwargs)
        self.p_exec = p_exec

    def __call__(self, *args, **kwargs):
        if random() < self.p_exec:
            return super().__call__(*args, **kwargs)


class Validate(partial):
    """
    Validates a participant's response.

    Attributes
    ----------
    error_msg : str or None
        If the validate function returns an error message, `error_msg` is 
        returned instead of the output of the validate function.
        You can set this by passing in an `error_msg` keyword argument to the
        constructor.

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
    def __init__(self, func, *args, error_msg=None, **kwargs):
        super().__init__(func, *args, **kwargs)
        self.error_msg = error_msg

    def __call__(self, *args, **kwargs):
        error_msg = super().__call__(*args, **kwargs)
        if error_msg:
            return self.error_msg or error_msg

            
class Submit(partial):
    """
    Runs after a participant has successfully submitted a page.

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


class Navigate(partial):
    """
    Creates a new branch to which the participant will navigate.

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