"""Hemlock survey"""

# import hemlock package, configuration class, and texts
from hemlock import *
from texts import *
from flask_login import current_user
    
def Start():
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, text='hello world')
    return b