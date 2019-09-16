"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root=None):
    b = Branch()
    p = Page(b)
    q = Question(p, text='hello world')
    
    p = Page(b)
    q = Question(p, text='hello star')
    
    p = Page(b, terminal=True)
    q = Question(p, text='goodbye moon')
    return b