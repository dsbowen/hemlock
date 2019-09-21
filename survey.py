"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root=None):
    b = Branch()
    p = Page(b)
    q = Question(p, qtype='single choice', text='test')
    Choice(q, text='Yes')
    Choice(q, text='No')
    
    q = Question(p, text='hello world')
    
    p = Page(b, terminal=True)
    q = Question(p, text='goodbye moon')
    return b

def require(question):
    if question.response is None:
        return '<p>Response required</p>'