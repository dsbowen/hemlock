"""Hemlock survey"""

from hemlock import *
from texts import *

@Settings.register('app')
def app_settings():
    return {
        'duplicate_keys': [],
        'password': '',
    }

@Settings.register('Page')
def settings():
    return {'back':True}

@route('/survey')
def Start(root=None):
    b = Branch()
    p = Page(b)
    p = Page(b)
    l = Label(p, label='<p>Hello World</p>', error='<p>Error</p>')
    l.error = None
    p = Page(b, terminal=True)
    return b