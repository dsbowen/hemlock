"""Hemlock survey"""

from hemlock import *
from texts import *

import hemlock_crt as crt

def Start(root=None):
    crt_b = crt.CRT(crt.ball_bat, crt.machines, crt.lily_pads)
    Navigate(crt_b, End)
    return crt_b

def End(root):
    b = Branch()
    p = Page(b, terminal=True)
    Text(p, text='<p>Thank you for completing this survey.</p>')
    return b