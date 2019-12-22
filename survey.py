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
        default='Default answer', 
        prepend='$',
        append='.00',
    )
    Input(p, label='<p>This is a textarea.</p>', textarea=True)
    s = Select(
        p,
        label='<p>This is a select question.</p>',
        prepend='Choose one.',
        choices=['Red', 'Blue', 'Green']
    )
    s.default = s.choices[1]
    s = Select(
        p,
        multiple=True,
        label='<p>This is also a select question. Choose as many as you like.</p>',
        choices=['World', 'Moon', 'Sun', 'Star', 'Galaxy']
    )
    s.default = s.choices[0:2]
    s.select['size'] = 7
    Check(
        p,
        label='<p>This is a form-check group.</p>',
        choices=['Hello', 'World']
    )
    Check(
        p,
        prepend='Choose two.',
        label='<p>Hello world.</p>',
        choices=['Goodbye', 'Moon'],
        multiple=True
    )
    Check(
        p,
        inline=True,
        center=True,
        label='<p>Inline.</p>',
        choices=[str(i) for i in range(1,6)]
    )
    p = Page(b, terminal=True)
    return b