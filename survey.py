"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root=None):
    b = Branch()
    p = Page(b)
    q = Question(p, qtype='free', text='free response question')
    print('free id is', q.id)
    
    q = Question(p, qtype='single choice', text='single choice question')
    Choice(q, text='Yes')
    Choice(q, text='No')
    print('single id is', q.id)
    
    q = Question(p, qtype='multi choice', text='multi choice question')
    Choice(q, text='Yes')
    Choice(q, text='No')
    print('multi id is', q.id)
    
    p = Page(b, terminal=True)
    q = Question(p, text='goodbye moon')
    return b

def require(question):
    if question.response is None:
        return '<p>Response required</p>'