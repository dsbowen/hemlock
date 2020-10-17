from hemlock import Branch, Compile as C, Page, Label, Input, Validate as V, Navigate as N, route
from sqlalchemy_mutable import partial

@route('/survey')
def start():
    inpt = Input(
        "<p>What's your name?</p>", 
        validate=V.require(error_msg='<p>ERROR!</p>'), 
        submit=uppercase
    )
    return Branch(
        Page(
            inpt,
        ),
        Page(
            Label(compile=partial(greet, inpt)),
            navigate=middle
        ),
        navigate=end
    )

def middle(branch):
    return Branch(
        Page(
            Label(
                '<p>Middle</p>'
            )
        )
    )

def end(branch):
    return Branch(
        Page(
            Label(
                'the end'
            ),
            terminal=True
        )
    )

def uppercase(q):
    q.response = q.response.upper()

def greet(greet_q, name_q):
    greet_q.label = name_q.response