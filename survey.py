"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root=None):
    b = Branch()
    
    p = Page(b)
    q = Question(p, text='Intro')
    
    p = Page(b)
    q = Question(p, var='free', type='free', text='free response question')
    
    q = Question(
        p, var='single', type='single choice', text='single choice question')
    Choice(q, text='Yes')
    Choice(q, text='No')
    
    q = Question(
        p, var='multi', type='multi choice', text='multi choice question')
    Choice(q, text='Yes')
    Choice(q, text='No')
    
    p = Page(b, terminal=True)
    q = Question(p, text='goodbye moon')
    return b

def require(question):
    if question.response is None:
        return '<p>Response required</p>'