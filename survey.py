"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root):
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, text='hello world')
    return b