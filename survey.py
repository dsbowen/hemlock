"""Hemlock survey"""

from hemlock import *
from texts import *

def Start(root=None):
    b = Branch()
    p = Page(b)
    Text(p, text='Hello World')
    f = Free(p)
    Validate(f, require)
    p = Page(b, terminal=True)
    Text(p, text='Goodbye World')
    return b