"""Hemlock survey"""

from hemlock import *
from texts import *

def Start(root=None):
    b = Branch()
    p = Page(b)
    Text(p, text='Hello World!')
    Download(p, text='Hello World')
    Navigate(b, Branch2)
    return b

def Branch2(root):
    b = Branch()
    p = Page(b, terminal=True)
    Text(p, text='Goodbye World!')
    return b