"""Hemlock survey"""

from hemlock import *
from texts import *

def Start(root=None):
    b = Branch()
    p = Page(b)
    sc = SingleChoice(p, text='Yes or No?', var='Yes')
    Choice(sc, text='Yes')
    Choice(sc, text='No')

    p = Page(b, terminal=True)
    txt = Text(p, text='The End')
    return b