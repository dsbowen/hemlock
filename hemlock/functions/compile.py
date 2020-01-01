"""Compile functions"""

from hemlock.database import Compile

from random import shuffle

@Compile.register
def rerandomize(obj):
    """Rerandomize

    If the object is a `Page`, shuffle its `questions`.
    If the object is a `ChoiceQuestion`, shuffle its `choices`.
    """
    if hasattr(obj, 'questions'):
        shuffle(obj.questions)
    elif hasattr(obj, 'choices'):
        shuffle(obj.choices)

@Compile.register
def clear_error(obj):
    obj.clear_error()

@Compile.register
def clear_response(obj):
    obj.clear_response()