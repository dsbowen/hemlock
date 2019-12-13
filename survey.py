"""Hemlock survey"""

from hemlock import *
from texts import *

def Start(root=None):
    b = Branch()
    p = Page(b)
    Text(p, text='Goodbye world')
    free_q = Free(p)
    Validate(free_q, numeric)
    p = Page(b, terminal=True)
    Text(p, text='Hello World')
    return b