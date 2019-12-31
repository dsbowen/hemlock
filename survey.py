"""Hello World: a starting example"""

import questions

from hemlock import *

# @route('/survey')
# def Start(origin=None):
#     b = Branch()
#     p = Page(b, terminal=True)
#     Label(p, label='Hello World')
#     return b

# @route('/survey')
def Start(origin=None):
    b = Branch()
    Navigate.QuestionPolymorphs(b)
    p = Page(b)
    Label(p, label='Hello World')
    return b

@Navigate.register
def End(origin=None):
    b = Branch()
    p = Page(b, terminal=True)
    Label(p, label='Goodbye World')
    return b