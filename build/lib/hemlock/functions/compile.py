"""## Compile functions"""

from ..models import Compile, Page, ChoiceQuestion

from random import shuffle as shuffle_

@Compile.register
def call_method(obj, method_name, *args, **kwargs):
    """
    Calls one of the object's methods.

    Parameters
    ----------
    obj :
        Object whose methods will be called.

    method_name : str
        Names of the method to call.

    \*args, \*\*kwargs :
        Arguments and keyword arguments to pass to the method.

    Examples
    --------
    ```python
    from hemlock import Compile as C, Page, push_app_context

    app = push_app_context()

    p = Page(error='Error message', compile=C.call_method('clear_error'))
    p.preview()._compile().preview()
    ```
    """
    getattr(obj, method_name)(*args, **kwargs)

@Compile.register
def clear_error(obj):
    """
    Calls the object's `clear_error` method.

    Parameters
    ----------
    obj :
        Object whose `clear_error` method will be called.

    Examples
    --------
    ```python
    from hemlock import Compile as C, Page, push_app_context

    app = push_app_context()

    p = Page(error='Error message', compile=C.clear_error())
    p.preview()._compile().preview()
    ```
    """
    obj.clear_error()

@Compile.register
def clear_response(obj):
    """
    Calls the object's `clear_response` method.

    Parameters
    ----------
    obj :
        Object whose `clear_response` method will be called.

    Examples
    --------
    ```python
    from hemlock import Compile as C, Input, Page, push_app_context

    app = push_app_context()

    p = Page(Input(response='Hello World'), compile=C.clear_response())
    p.preview()._compile().preview()
    ```
    """
    obj.clear_response()

@Compile.register
def shuffle(obj, *attrs):
    """
    Shuffle an object's attributes.

    Parameters
    ----------
    obj :
        Objects whose attributes should be shuffled.

    \*attrs : str
        Names of attributes to shuffle.

    Notes
    -----
    If the object is a `hemlock.Page`, the default shuffled attribute is its 
    `questions`.

    If the object is a `hemlock.ChoiceQuestion`, the default shuffled
    attribute is its `choices`.

    Examples
    --------
    ```python
    from hemlock import Compile as C, Label, Page, push_app_context

    app = push_app_context()

    p = Page(
    \    *(Label('<p>Label {}</p>'.format(i)) for i in range(4)),
    \    compile=C.shuffle()
    )
    p.preview()._compile().preview()
    ```
    """
    if not attrs:
        if isinstance(obj, Page):
            attrs = ['questions']
        elif isinstance(obj, ChoiceQuestion):
            attrs = ['choices']
    [shuffle_(getattr(obj, attr)) for attr in attrs]