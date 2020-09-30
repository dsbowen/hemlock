from hemlock import Branch, Page, Check, Input, Label, Select, Submit as S, route
from hemlock.tools import show_on_event

@route('/survey')
def start():
    country_q = Select(
        'Select your country',
        ['United States', 'Other']
    )
    specify_q = Input(
        'Please specify'
    )
    show_on_event(specify_q, country_q, 'Other')
    return Branch(
        Page(
            country_q, specify_q
        ),
        Page(
            Label('<p>The end.</p>'),
            back=True,
            terminal=True
        )
    )

def print_resp_data(q):
    print(q.response)
    print(q.data)