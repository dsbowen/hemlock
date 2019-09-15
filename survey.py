"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root):
    b = Branch(navigate=End)
    p = Page(b, navigate=Nav1)
    q = Question(p, text='hello world')
    return b
    
def Nav1(b):
    b = Branch()
    return b

def End(b):
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, text='goodbye world')
    return b