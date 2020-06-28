"""## Compile functions"""

from ..models import Compile, Page, ChoiceQuestion

from random import shuffle

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
    """
    if not attrs:
        if isinstance(obj, Page):
            attrs = ['questions']
        elif isinstance(obj, ChoiceQuestion):
            attrs = ['choices']
    [shuffle(getattr(obj, attr)) for attr in attrs]