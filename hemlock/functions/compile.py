"""Compile functions"""

from hemlock.database import Compile

from random import shuffle

@Compile.register
def rerandomize(obj):
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