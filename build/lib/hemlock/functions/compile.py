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
    from hemlock import Compile, Page, push_app_context

    push_app_context()

    p = Compile.call_method(Page(error='Error message'), 'clear_error')
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
    from hemlock import Compile, Page, Check, push_app_context

    push_app_context()

    p = Compile.clear_error(Page(error='Error message'))
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
    from hemlock import Compile, Input, Page, push_app_context

    push_app_context()

    p = Compile.clear_response(Page(Input(response='Hello World')))
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
    from hemlock import Compile, Label, Page, push_app_context

    push_app_context()

    p = Compile.shuffle(Page(
    \    Label('<p>Label {}</p>'.format(i)) for i in range(4)
    ))
    p.preview()._compile().preview()
    ```
    """
    if not attrs:
        if isinstance(obj, Page):
            attrs = ['questions']
        elif isinstance(obj, ChoiceQuestion):
            attrs = ['choices']
    [shuffle_(getattr(obj, attr)) for attr in attrs]