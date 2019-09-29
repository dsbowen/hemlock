"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
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
    Choice(q, text='Yes')
    Choice(q, text='No')
    
    p = Page(b, terminal=True)
    q = Text(p, text='goodbye moon')
    return b

def require(question):
    if question.response is None:
        return '<p>Response required</p>'