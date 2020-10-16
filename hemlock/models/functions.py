"""# Function models"""

from sqlalchemy_mutable import Mutable, partial

from random import random


class MutableFunctionBase(Mutable):
    def __init__(self, source=None, root=None):
        super().__init__(source.func, *source.args, **source.kwargs)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.func.__name__)


class Compile(partial):
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


@Mutable.register_tracked_type(Compile)
class CompileFunction(MutableFunctionBase, Compile):
    pass


class Debug(partial):
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
    def __init__(self, *args, **kwargs):
        self.p_exec = kwargs.pop('p_exec', 1.)
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Execute the debug function with probability `self.p_exec`.
        """
        if random() < self.p_exec:
            return super().__call__(*args, **kwargs)


@Mutable.register_tracked_type(Debug)
class DebugFunction(MutableFunctionBase, Debug):
    pass


class Validate(partial):
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


@Mutable.register_tracked_type(Validate)
class ValidateFunction(MutableFunctionBase, Validate):
    pass

            
class Submit(partial):
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


@Mutable.register_tracked_type(Submit)
class SubmitFunction(MutableFunctionBase, Submit):
    pass


class Navigate(partial):
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
    def __call__(self, origin, *args, **kwargs):
        """
        Create a new branch and 'link' it to the tree. Linking in the new 
        branch involves setting the `next_branch` and `origin_branch` or 
        `origin_page` relationships.
        """
        from .branch import Branch

        next_branch = super().__call__(origin, *args, **kwargs)
        assert isinstance(next_branch, Branch)
        self._set_relationships(origin, next_branch)
        next_branch.current_page = next_branch.start_page
        return next_branch

    def _set_relationships(self, origin, next_branch):
        """Set relationships between next_branch and its origin"""
        from .branch import Branch

        origin.next_branch = next_branch
        if isinstance(origin, Branch):
            next_branch.origin_page = None
            next_branch.origin_branch = origin
        else:
            # origin is hemlock.Page
            next_branch.origin_branch = None
            next_branch.origin_page = origin


@Mutable.register_tracked_type(Navigate)
class NavigateFunction(MutableFunctionBase, Navigate):
    pass