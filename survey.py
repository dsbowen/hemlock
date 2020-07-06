"""Hello World: a starting example"""

# import questions

from hemlock import Branch, Page, Label, Input, Validate, route

@route('/survey')
def start():
    return Branch(
        Page(Validate.require(Input('<p>Required</p>'))),
        Page(Label('<p>The End!</p>'), terminal=True)
    )