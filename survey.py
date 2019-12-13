"""Hemlock survey"""

from hemlock import *
from texts import *

from hemlock_crt import CRT, ball_bat, machines, lily_pads

def Start(root=None):
    b = CRT(ball_bat, machines, lily_pads)
    Navigate(b, IPD)
    x=1/0
    return b

def IPD(root=None):
    b = Branch()
    p = Page(b, terminal=True)
    Text(p, text='Hello World')
    return b