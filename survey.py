"""Hemlock survey"""

from hemlock import *
from texts import *

from flask_login import current_user
from random import shuffle

def Start(root=None):
    b = Branch()
    
    p = Page(b)
    q = Text(p, text='Intro')
    
    p = Page(b)
    q = Free(p, var='free', text='free response question')
    
    q = SingleChoice(p, var='single', text='single choice question')
    Choice(q, text='Yes')
    Choice(q, text='No')
    
    q = MultiChoice(p, var='multi', text='multi choice question')
    q.compile = rerandomize
    Choice(q, text='Red')
    Choice(q, text='Blue')
    y = Choice(q, text='Yellow')
    q.default = [y]
    
    p = Page(b, terminal=True)
    q = Text(p, text='goodbye moon')
    return b

def rerandomize(question):
    shuffle(question.choices)