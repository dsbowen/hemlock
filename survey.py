"""Hemlock survey"""

from hemlock import *
from texts import *

def Start(root=None):
    b = Branch()
    p = Page(b)
    Text(p, text='Hello World!')
    Navigate(b, End)
    return b

def End(root):
    b = Branch()
    p = Page(b, terminal=True)
    Text(p, text='Goodbye World!')
    return b