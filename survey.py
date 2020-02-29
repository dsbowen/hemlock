"""Hello World: a starting example"""

import questions

from hemlock import *

from random import choice

@route('/survey')
def Start(origin=None):
    b = Branch()
    Navigate.QuestionPolymorphs(b)
    p = Page(b)
    Label(p, label='<p>Hello World</p>')
    return b

@Navigate.register
def End(origin=None):
    b = Branch()
    p = Page(b, terminal=True)
    Label(p, label='<p>Thank you for completing the Hemlock tutorial.</p>')
    return b