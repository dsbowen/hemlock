"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root):
    b = Branch(navigate=End)
    p = Page(b, navigate=Nav1)
    p = Page(b)
    p = Page(b)
    return b
    
def Nav1(b):
    b = Branch(navigate=Nav2)
    return b
    
def Nav2(b):
    b = Branch()
    return b

def End(b):
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, text='goodbye world')
    return b