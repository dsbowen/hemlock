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
    Input(p, label='<p>This is a text input.</p>')
    Input(p, label='<p>This is an date input.</p>', input_type='date')
    Input(p, label='<p>This is a color input.</p>', input_type='color')
    Input(
        p, 
        label='<p>This is a text input with prepended and appended text.</p>', 
        prepend='$', 
        append='.00',
    )
    Input(p, label='<p>This is a textarea.</p>', textarea=True)
    # s = Select(
    #     p,
    #     label='<p>This is a select question.</p>',
    #     prepend='Choose one.',
    #     choices=['Red', 'Blue', 'Green']
    # )
    p = Page(b, terminal=True)
    return b