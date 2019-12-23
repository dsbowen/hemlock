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
def End(root=None):
    b = Branch()
    p = Page(b)
    i = Input(p, label='<p>Enter an integer.</p>')
    Validate(i, is_type, args=[int])
    i = Input(p, label='<p>Enter a number less than 100.</p>')
    Validate(i, max_val, kwargs={'max': 100, 'resp_type': float})
    i = Input(p, label='<p>Enter a number greater than 0.</p>')
    Validate(i, min_val, kwargs={'min': 0, 'resp_type': float})
    i = Input(p, label='<p>Enter a number between 0 and 100.</p>')
    Validate(i, range_val, kwargs={'min': 0, 'max': 100, 'resp_type': float})
    t = Textarea(p, label='<p>Enter a maximum of 10 characters.</p>')
    Validate(t, max_len, args=[10])
    t = Textarea(p, label='<p>Enter at least 5 characters.</p>')
    Validate(t, min_len, args=[5])
    t = Textarea(p, label='<p>Enter between 5 and 10 characters.</p>')
    Validate(t, range_len, args=[5,10])
    s = Select(
        p,
        label='<p>Select a maximum of 2 choices.</p>',
        multiple=True,
        choices=['Red','Blue','Green']
    )
    Validate(s, max_len, args=[2])
    c = Check(
        p,
        label='<p>Select a minimum of 1 choice.</p>',
        multiple=True,
        choices=['Red','Blue','Green']
    )
    Validate(c, min_len, args=[1])
    t = Textarea(p, label='<p>Enter at most 3 words.</p>')
    Validate(t, max_words, args=[3])
    t = Textarea(p, label='<p>Enter at least 1 word.</p>')
    Validate(t, min_words, args=[1])
    t = Textarea(p, label='<p>Enter between 1 and 3 words.</p>')
    Validate(t, range_words, args=[1,3])
    i = Input(p, label='<p>Enter a proper noun.</p>')
    Validate(i, regex, args=['([A-Z])\w+'])
    i = Input(p, label='<p>Enter one of the following: Red, Green, Blue.</p>')
    Validate(i, is_in, args=[['Red','Green','Blue']])
    i = Input(p, label='<p>Do not enter one of the following: Red, Green, Blue.</p>')
    Validate(i, is_not_in, args=[['Red','Green','Blue']])
    i = Input(p, label='<p>Enter a dollar and cents.</p>', prepend='$')
    Validate(i, exact_decimals, args=[2])
    i = Input(p, label='<p>Enter a number with 0 decimals.</p>')
    Validate(i, max_decimals, args=[0])
    i = Input(p, label='<p>Enter a number with at least 1 decimal.</p>')
    Validate(i, min_decimals, args=[1])
    i = Input(p, label='<p>Enter a number with between 0 and 3 decimals.</p>')
    Validate(i, range_decimals, args=[0,3])
    p = Page(b, terminal=True)
    return b

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
    Textarea(p, label='<p>This is a textarea.</p>')
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
        choices=list(range(1,6))
    )
    Check(
        p,
        inline=True,
        center=True,
        multiple=True,
        choices=['John','Kim','Dillon']
    )
    Range(p, label='<p>This is a range.</p>', max=5, step=.5)
    p = Page(b, terminal=True)
    return b