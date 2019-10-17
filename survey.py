"""Hemlock survey"""

from hemlock import *
from texts import *

from flask_login import current_user
from random import shuffle

def Start():
    b = Branch()
    p = Page(b)
    Compile(p, complex_task, args=[5])
    CompileWorker(p)
    q = Text(p, text='Hello World')
    return b

import time
def complex_task(page, seconds):
    for i in range(seconds):
        print(100.0*i/seconds)
        time.sleep(1)