"""Hemlock survey"""

from hemlock import *
from texts import *

from flask_login import current_user
from random import shuffle

def Start(root=None):
    b = Branch()
    
    p = Page(b)
    q = Text(p, text='Intro')
    
    p = Page(b, compile_worker=True, validator_worker=True, submit_worker=True)
    q = Free(p, var='free', text='free response question')
    Validator(q, require)
    
    q = SingleChoice(p, var='single', text='single choice question')
    Choice(q, text='Yes')
    Choice(q, text='No')
    
    q = MultiChoice(p, var='multi', text='multi choice question')
    CompileFunction(q, rerandomize)
    CompileFunction(q, clear_response)
    Choice(q, text='Red')
    Choice(q, text='Blue')
    Choice(q, text='Yellow')
    
    p = Page(b, terminal=True)
    q = Text(p, text='goodbye moon')
    return b

def require(question):
    if question.response is None:
        return 'Hey, answer the damn question!'

def rerandomize(question):
    shuffle(question.choices)

def clear_response(question):
    question.response = None