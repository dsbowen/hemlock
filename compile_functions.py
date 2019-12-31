"""Compile functions

Compile functions run just before a `Page` is compiled.
"""

import submit_functions

from hemlock import *

def CompileFunctions(origin=None):
    b = Branch()
    Navigate.SubmitFunctions(b)

    """Rerandomize"""
    p = Page(b)
    Label(p, label='<p>Click refresh to rerandomize the label order.</p>')
    Label(p, label='<p>This is another label.</p>')
    Compile.rerandomize(p)

    p = Page(b)
    c = Check(
        p,
        label='<p>Click refresh to rerandomize the choice order.</p>',
        choices=['World','Moon','Star']
    )
    Compile.rerandomize(c)

    """Clear error"""
    p = Page(b)
    i = Input(
        p, 
        label='<p>This input is required. But the error message is always cleared before it appears on the page.</p>'
    )
    Compile.clear_error(i)
    Validate.require(i)

    """Clear response"""
    p = Page(b)
    Label(
        p,
        label="""
        <p>By default, question responses are recorded when going forward or back.</p>
        <p>Sometimes, you may want to clear these responses.</p>
        """
    )
    Input(p, label='<p>Whatever you enter in this input will be cleared each time this page is compiled.</p>')
    Check(
        p, 
        label='<p>It also works for choice questions.</p>',
        choices=list(range(1,6)),
        inline=True,
        center=True
    )
    Compile.clear_response(p)


    """Custom compile functions"""
    p = Page(b)
    Label(p, label='<p>This greeting requires a user-defined compile function.</p>')
    name = Input(p, label="<p>What's your name?</p>")

    p = Page(b)
    greeting = Label(p)
    Compile.greet(greeting, name)

    return b

@Compile.register
def greet(greeting, name):
    greeting.label = 'Hello, {}!'.format(name.response)