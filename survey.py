from hemlock import Branch, Check, Compile as C, Page, Label, Input, Validate as V, Navigate as N, route
from sqlalchemy_mutable import partial
from hemlock_demographics import comprehensive_demographics

@route('/survey')
def start():
    return Branch(
        comprehensive_demographics(page=True),
        navigate=end
    )

def middle(branch):
    return Branch(
        Page(
            Label(
                'Middle'
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