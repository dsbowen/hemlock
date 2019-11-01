"""Hemlock survey"""

from hemlock import *
from texts import *

from flask_login import current_user
from random import shuffle

def Start(root=None):
    b = Branch()
    p = Page(b, terminal=True)
    Text(p, text='Hello World!')
    return b