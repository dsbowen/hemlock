"""Hemlock survey"""

from hemlock import *
from texts import *

from flask_login import current_user
from random import shuffle

def Start():
    b = Branch()
    p1 = Page(b)
    Navigate(p1, Branch2)
    NavigateWorker(p1)
    q = Text(p1, text='Hello World')

    p2 = Page(b)
    q = Text(p2, text='goodbye world')

    p1.forward_to = p2

    return b

def Branch2(root):
    b = Branch()
    Navigate(b, Branch3)
    NavigateWorker(b)
    p = Page(b)
    q = Text(p, text='hello moon')
    return b

def Branch3(root):
    b = Branch()
    p = Page(b)
    q = Text(p, text='hello star')
    return b