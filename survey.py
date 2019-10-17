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
    Text(p1, text='Hello World')
    mc = MultiChoice(p1, text='Multi choice')
    mc.error = 'Test error'
    Choice(mc, text='Red')
    Choice(mc, text='Blue')
    Choice(mc, text='Yellow')
    sc = SingleChoice(p1, text='Single choice')
    Choice(sc, text='Yes')
    Choice(sc, text='No')
    Free(p1)

    p2 = Page(b, terminal=True)
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
    Submit(p, go_invalid)
    q = Text(p, text='hello star')
    return b

def go_invalid(page):
    page.error = 'Error message'
    page.direction_from = 'invalid'