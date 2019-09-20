"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root=None):
    b = Branch()
    p = Page(b, timer_var='v1', all_rows=True)
    q = Question(p, qtype='free', text='name', var='Name', all_rows=True)
    v = Validator(q, validate=require)
    
    p = Page(b, terminal=True)
    q = Question(p, text='goodbye moon')
    return b

def require(question):
    if question.response is None:
        return '<p>Response required</p>'