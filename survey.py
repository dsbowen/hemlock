"""Hello World: a starting example"""

import questions

from hemlock import *

from random import choice

@Settings.register('app')
def settings():
    return {'validation': True}

@route('/survey')
def Start(origin=None):
    b = Branch()
    # Navigate.QuestionPolymorphs(b)
    Navigate.End(b)
    p = Page(b)
    i = Input(p, label='required')
    Validate.require(i)
    Label(p, label='<p>Hello World</p>')
    return b

@Navigate.register
def End(origin=None):
    b = Branch()
    p = Page(b, terminal=True)
    Label(p, label='<p>Thank you for completing the Hemlock tutorial.</p>')
    return b