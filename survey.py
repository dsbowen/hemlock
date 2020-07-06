"""Hello World: a starting example"""

# import questions

from hemlock import Branch, File, Page, Label, route
import os

print(os.environ.get('NO_DEBUG_FUNCTIONS'))

@route('/survey')
def start():
    return Branch(
        Page(Label('<p>Hello moon</p>')),
        Page(Label('<p>The End</p>'), terminal=True)
    )