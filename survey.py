"""Hello World: a starting example"""

# custom submit converts to datetime and adds embedded for age
# UG:
    # navigate and compile
    # assign
# data and timers
# debugging
# deployment

from hemlock import Branch, Check, Input, Page, Label, Range, Select, Validate, route

from datetime import datetime

@Validate.register
def validate_date_format(inpt):
    try:
        # try to convert to a datetime object
        datetime.strptime(inpt.response, '%m/%d/%Y')
    except:
        # if this fails, the participant entered an invalid response
        return '<p>Make sure to format your date of birth as mm/dd/yyyy.</p>'

@route('/survey')
def start():
    return Branch(
        Page(
            Validate.validate_date_format(Validate.require(Input(
                '<p>Please enter your date of birth in mm/dd/yyyy format.</p>'
            ))),
            Validate.require(Check(
                '<p>Please indicate your gender.</p>',
                ['Male', 'Female', 'Other']
            )),
            Validate.require(Check(
                '<p>Please indicate your ethnicity. Check as many as apply.</p>',
                [
                    'White',
                    'Black or African-American',
                    'Asian',
                    'Native Hawaiian or other Pacific Islander',
                    'Other',
                ],
                multiple=True
            )),
            Validate.require(Select(
                '<p>Please select your current marital status.</p>',
                [
                    'Married',
                    'Widowed',
                    'Divorced',
                    'Separated',
                    'Never married',
                ]
            )),
            Range(
                '''
                <p>At the right end of the scale are the people who are the 
                best off; those who have the most money, the most 
                education, and the best jobs. On the left are the people 
                who are the worst off; those who have the least money, the 
                least education, and the worst jobs (or are unemployed). 
                Please indicate where you think you stand on this scale.</p>
                ''',
                min=0, max=10
            ),
        ),
        Page(
            Label('<p>Thank you for completing this survey.</p>'), 
            terminal=True
        )
    )