"""Hemlock survey"""

from hemlock import *
from texts import *

def Start(root=None):
    b = Branch()
    p = Page(b)
    CompileWorker(p)
    Text(p, text='Hello World!')
    Navigate(b, Branch2)
    return b

def Branch2(root):
    b = Branch()
    p = Page(b, terminal=True)
    Text(p, text='Goodbye World!')
    return b