from hemlock import Branch, Page, Input, Label, Compile as C, Range, Embedded, route
from hemlock_demographics import demographics
from hemlock_berlin import berlin
from hemlock_crt import crt

@route('/survey')
def start():
    return Branch(
        demographics('age_bins', 'gender', 'race', page=True),
        berlin(),
        *crt(page=True),
        navigate=forecast
    )

# @route('/survey')
def forecast(origin=None):
    return Branch(
        Page(
            Range(
                'Fill in the blank: There is a _____ in 100 chance the high temperature in Philadelphia tomorrow will be greater than 50 degrees F.',
                prepend='There is a ', append=' in 100 chance', var='Temp'
            ),
            timer='Time'
        ),
        Page(
            Label('Thank you for completing the study'),
            terminal=True
        )
    )