"""Hemlock survey"""

from hemlock import *
from texts import *

@Settings.register('app')
def app_settings():
    return {
        'duplicate_keys': [],
        'password': '',
    }

@route('/survey')
def Start(root=None):
    b = Branch()
    p = Page(b, terminal=True)
    Free(p, label='Hello World', prepend='hello', append='world')
    return b