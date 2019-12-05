"""Hemlock survey"""

from hemlock import *
from texts import *

def Start(root=None):
    b = Branch()
    p = Page(b, terminal=True)
    Text(p, text='Hello World')
    return b