"""Submit functions

Just as compile functions run just before a `Page` is compile, submit 
functions run just after a `Page` is submitted.
"""

import validate_functions

from hemlock import *

def SubmitFunctions(origin=None):
    b = Branch()
    Navigate.End(b)

    input_p = Page(b)

    """Type conversion"""
    i = Input(
        input_p, 
        label='<p>The data for this input will be converted to an int.</p>'
    )
    Validate.is_type(i, int)
    Submit.data_type(i, int)

    """Regex matching"""
    i = Input(
        input_p, 
        label='<p>The data for this input indicates whether the response was "correct".</p>'
    )
    Submit.match(i, 'correct')

    """Correct choices"""
    s = Select(
        input_p,
        label='<p>The data for this question indicates whether the selected choice was correct.<p>'
    )
    Option(s, label='Incorrect', value=0)
    Option(s, label='Correct', value=1)
    Submit.correct_choices(s)

    """Custom Submit functions"""
    p = Page(b)
    Label(
        p,
        label='We can use a custom submit function to verify the behavior of the submit functions on the previous page.</p>'
    )
    display_data = Label(p)
    Submit.display_data(input_p, display_data)

    return b

@Submit.register
def display_data(input_page, display_data):
    label = ''

    if isinstance(input_page.questions[0].data, int):
        label += "<p>The first question's data was converted to an int.</p>"

    if input_page.questions[1].data == 1:
        label += '<p>Your response to the second question was "correct".</p>'
    else: # data == 0
        label += '<p>Your response to the second question was not "correct".</p>'
    
    if input_page.questions[2].data == 1:
        label += '<p>You selected the correct choice for the third question.</p>'
    else: # data == 0
        label += '<p>You did not select the correct choice for the third question.</p>'
    
    display_data.label = label