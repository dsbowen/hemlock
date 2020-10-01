from hemlock import Branch, Page, Check, Input, Label, Select, Submit as S, route
from hemlock.tools import show_on_event

@route('/survey')
def start():
    race = Check(
        '<p>Race</p>',
        ['White', 'Black', 'Other'],
        multiple=True
    )
    specify_race = Input('<p>Specify race</p>')
    show_on_event(specify_race, race, 'Other')
    gender = Select(
        '<p>Gender</p>',
        ['Male', 'Female', 'Other']
    )
    specify_gender = Input('<p>Specify gender</p>')
    show_on_event(specify_gender, gender, 'Other')
    return Branch(
        Page(
            race, specify_race, gender, specify_gender
        ),
        Page(
            Label('<p>The end.</p>'),
            back=True,
            terminal=True
        )
    )