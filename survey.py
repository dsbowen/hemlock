from hemlock import Branch, Page, Check, Input, Label, Select, Submit as S, route
from hemlock.tools import show_on_event

@route('/survey')
def start():
    return Branch(
        Page(
            Select(
                '<p>What year were you born in?</p>',
                list(range(1900, 2020))
            )
        ),
        Page(
            Label('<p>The end.</p>'),
            back=True,
            terminal=True
        )
    )