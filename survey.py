"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root=None):
    b = Branch()
    p = Page(b)
    q = Question(p, qtype='single choice', text='test')
    q.interval = Interval(func=random_number, seconds=2)
    Choice(q, text='Yes')
    Choice(q, text='No')
    
    p = Page(b, terminal=True)
    q = Question(p, text='goodbye moon')
    return b
    
from random import random
def random_number(question):
    question.text = str(random())

def require(question):
    if question.response is None:
        return '<p>Response required</p>'