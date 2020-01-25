"""Hello World: a starting example"""

import questions

from hemlock import *

from random import choice

@route('/survey')
def Start(origin=None):
    b = Branch()
    Navigate.End(b)

    p = Page(b)
    c = Check(
        p,
        name='preferred_color',
        label='<p>Which color do you prefer?</p>',
        choices=['Red', 'Blue']
    )
    Validate.require(c)

    p = Page(b, cache_compile=True)
    Compile.display_participant_response(p)

    return b

@Compile.register
def display_participant_response(page):
    color_questions = Check.query.filter_by(name='preferred_color').all()
    colors = [c.data for c in color_questions if c.data is not None]
    pct_red = int(100 * colors.count('Red') / len(colors))
    Label(
        page,
        label = '<p>A randomly selected participant preferred {}.</p>'.format(choice(colors))
    )
    Label(
        page,
        label = '<p>{}% of participants preferred Red.</p>'.format(pct_red)
    )

# @route('/survey')
# def Start(origin=None):
#     b = Branch()
#     p = Page(b, terminal=True)
#     Label(p, label='<p>Hello World</p>')
#     return b

# @route('/survey')
# def Start(origin=None):
#     b = Branch()
#     Navigate.QuestionPolymorphs(b)
#     p = Page(b)
#     Label(p, label='<p>Hello World</p>')
#     return b

@Navigate.register
def End(origin=None):
    b = Branch()
    p = Page(b, terminal=True)
    Label(p, label='<p>Thank you for completing the Hemlock tutorial.</p>')
    return b