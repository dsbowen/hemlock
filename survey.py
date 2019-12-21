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
    Label(p, label='<p>This is a label.</p>')
    t = Text(
        p, 
        label='<p>This is a text input.</p>', 
        prepend='$', 
        append='.00'
    )
    t = Text(
        p, 
        label='<p>This is a textarea.</p>', 
        default='Hello World', 
        textarea=True
    )
    p = Page(b, terminal=True)
    return b