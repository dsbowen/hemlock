"""Hemlock survey"""

from hemlock import *
from texts import *

@Settings.register('app')
def app_settings():
    return {
        'duplicate_keys': [],
        'password': '',
    }

@Settings.register('Page')
def settings():
    return {'back':True}

def Start(root=None):
    b = Branch()
    p = Page(b, terminal=True)
    Label(p, label='<p>Hello World.</p>')
    return b

@Navigate.register
def End(root=None):
    b = Branch()
    p = Page(b, terminal=True)
    Label(p, label='<p>Goodbye World.</p>')
    return b

def QuestionPolymorphs(root=None):
    b = Branch()
    Navigate.End(b)
    
    """Inputs and Textarea"""
    p = Page(b)
    Input(p, label='<p>Inputs default to text inputs.</p>')
    Input(p, label='<p>This is an date input.</p>', input_type='date')
    Input(p, label='<p>This is a time input.</p>', input_type='time')
    Input(p, label='<p>This is a color input.</p>', input_type='color')
    Input(
        p, 
        label='<p>Enter a dollar amount.</p>',
        prepend='$',
        default=100,
        append='.00',
    )
    Textarea(p, label='<p>This is a textarea.</p>', rows=5)

    """Choice questions"""
    p = Page(b)
    Select(
        p,
        label='<p>Select one.</p>',
        choices=['Red','Green','Blue']
    )
    Select(
        p,
        multiple=True,
        label='<p>Select multiple.</p>',
        choices=['World','Moon','Sun']
    )
    Check(
        p,
        label='<p>Select one.</p>',
        choices=[1, 2, 3]
    )
    Check(
        p,
        label='<p>Select multiple.</p>',
        choices=['Goodbye', 'Moon'],
        multiple=True
    )
    Check(
        p,
        label='<p>Display all options is a line.</p>',
        inline=True,
        center=True,
        choices=list(range(1,6))
    )
    s = Select(p, label='<p>With defaults.</p>')
    Option(s, label='Option 1', value=1)
    Option(s, label='Option 2', value=2)
    s.default = Option(s, label='Option 3', value=3)

    """Range"""
    p = Page(b)
    Range(p, label='<p>This is a range input.</p>')
    Range(
        p,
        label='<p>This range input goes from -10 to 10 in increments of 2.</p>',
        min=-10,
        max=10,
        step=2,
        default=-10
    )

    return b

def Validation(root=None):
    b = Branch()
    Navigate.End(b)

    """Require and type validation"""
    p = Page(b)
    i = Input(p, label='<p>Enter anything you like.</p>')
    Validate.require(i)
    i = Input(p, label='<p>Enter an integer.</p>')
    Validate.is_type(i, int)

    """Set validation"""
    p = Page(b)
    i = Input(p, label='<p>Enter 1, 2, or 3.</p>')
    Validate.is_in(i, ['1', '2', '3'])
    i = Input(p, label='<p>Do not enter 2 or 3.</p>')
    Validate.is_not_in(i, ['2','3'])

    """Range validation"""
    p = Page(b)
    i = Input(p, label='<p>Enter a number less than 100.</p>')
    Validate.max_val(i, 100, resp_type=float)
    i = Input(p, label='<p>Enter a number greater than 0.</p>')
    Validate.min_val(i, 0, resp_type=float)
    i = Input(p, label='<p>Enter a number between 0 and 100.</p>')
    Validate.range_val(i, min=0, max=100, resp_type=float)

    """Length and number of choices validation"""
    p = Page(b)
    t = Textarea(p, label='<p>Enter a maximum of 10 characters.</p>')
    Validate.max_len(t, 10)
    t = Textarea(p, label='<p>Enter at least 5 characters.</p>')
    Validate.min_len(t, 5)
    t = Textarea(p, label='<p>Enter between 5 and 10 characters.</p>')
    Validate.range_len(t, min=5, max=10)
    t = Textarea(p, label='<p>Enter exactly 7 characters.</p>')
    Validate.exact_len(t, 7)
    s = Select(
        p,
        label='<p>Select at most 2 choices.</p>',
        multiple=True,
        choices=['Red','Green','Blue']
    )
    Validate.max_len(s, 2)
    c = Check(
        p,
        label='<p>Select at least 1 choice.</p>',
        multiple=True,
        choices=['Red','Green','Blue']
    )
    Validate.min_len(c, 1)
    s = Select(
        p,
        label='<p>Select between 2 and 3 choices.</p>',
        multiple=True,
        choices=['World','Moon','Star']
    )
    Validate.range_len(s, min=2, max=3)
    c = Check(
        p,
        label='<p>Select exactly 2 choices.</p>',
        multiple=True,
        choices=['World','Moon','Star']
    )
    Validate.exact_len(c, 2)

    """Number of words validation"""
    p = Page(b)
    t = Textarea(p, label='<p>Enter at most 3 words.</p>')
    Validate.max_words(t, 3)
    t = Textarea(p, label='<p>Enter at least 1 word.</p>')
    Validate.min_words(t, 1)
    t = Textarea(p, label='<p>Enter between 1 and 3 words.</p>')
    Validate.range_words(t, min=1, max=3)
    t = Textarea(p, label='<p>Enter exactly 2 words.</p>')
    Validate.exact_words(t, 2)

    """Decimal validation"""
    p = Page(b)
    i = Input(p, label='<p>Enter a number with at most 3 decimals.</p>')
    Validate.max_decimals(i, 3)
    i = Input(p, label='<p>Enter a number with at least 1 decimal.</p>')
    Validate.min_decimals(i, 1)
    i = Input(p, label='<p>Enter a number with between 0 and 3 decimals.</p>')
    Validate.range_decimals(i, min=0, max=3)
    i = Input(
        p,
        label='<p>Enter a number with exactly 2 decimals.</p>',
        prepend='$'
    )
    Validate.exact_decimals(i, 2)

    """Regex validation"""
    p = Page(b)
    i = Input(p, label='<p>Enter a proper noun.</p>')
    Validate.match(i, pattern='([A-Z])\w+')

    return b

def CustomValidation(root=None):
    b = Branch()
    Navigate.End(b)

    """Question validation"""
    p = Page(b)
    password = Input(p, label='<p>Enter your password.</p>')
    confirm = Input(p, label='<p>Confirm password.</p>')
    Validate.confirm_password1(confirm, password)

    """Page validation"""
    p = Page(b)
    password = Input(p, label='<p>Enter your password.</p>')
    confirm = Input(p, label='<p>Confirm password.</p>')
    Validate.confirm_password2(p, password, confirm)

    return b

@Validate.register
def confirm_password1(confirm, password):
    if password.response != confirm.response:
        return '<p>Passwords must match.</p>'

@Validate.register
def confirm_password2(p, password, confirm):
    if password.response != confirm.response:
        return 'Passwords must match.'

def Compilation(root=None):
    b = Branch()
    Navigate.End(b)

    """Rerandomize"""
    p = Page(b)
    Label(p, label='<p>Click refresh to rerandomize the label order.</p>')
    Label(p, label='<p>This is another label.</p>')
    Compile.rerandomize(p)

    p = Page(b)
    c = Check(
        p,
        label='<p>Click refresh to rerandomize the choice order.</p>',
        choices=['Red','Green','Blue']
    )
    Compile.rerandomize(c)

    """Clear error"""
    p = Page(b)
    i = Input(
        p, 
        label='<p>This input is required, but no error message will be displayed.</p>'
    )
    Compile.clear_error(i)
    Validate.require(i)

    """Clear response"""
    p = Page(b)
    Input(p, label='<p>This response is cleared before compiling.</p>')
    Check(
        p, 
        label='<p>This response is also cleared before compiling.</p>',
        choices=['World','Moon','Sun']
    )
    Compile.clear_response(p)

    return b

def CustomCompilation(root=None):
    b = Branch()
    Navigate.End(b)

    p = Page(b)
    name = Input(p, label="<p>What's your name?</p>")

    p = Page(b)
    greeting = Label(p)
    Compile.greet(greeting, name)

    return b

@Compile.register
def greet(greeting, name):
    greeting.label = 'Hello, {}!'.format(name.response)

def Submission(root=None):
    b = Branch()
    Navigate.End(b)

    input_p = Page(b)
    integer = Input(
        input_p, 
        label='<p>The data for this input will be converted to an int.</p>'
    )
    Validate.is_type(integer, int)
    Submit.data_type(integer, int)
    correct = Input(
        input_p, 
        label='<p>The data for this input indicates whether the response was "correct".</p>'
    )
    Submit.match(correct, 'correct')

    p = Page(b)
    display_data = Label(p)

    Submit.display_data(input_p, integer, correct, display_data)

    return b

@Submit.register
def display_data(input_page, integer, correct, display_data):
    assert isinstance(integer.data, int)
    display_data.label = (
        '<p>The data for `integer` is {0}.</p>'
        +'<p>The data for `correct` is {1}.</p>'
    ).format(integer.data, correct.data)

@route('/survey')
def Debugging(root=None):
    b = Branch()
    Navigate.End(b)

    """Textarea and text Input"""
    p = Page(b)
    Textarea(p)
    Input(p, label='<p>This input accepts any input.</p>')
    i = Input(p, label='<p>This input accepts any number.</p>')
    Validate.is_type(i, float)
    Debug.random_number(i)
    i = Input(p, label='<p>This input accepts integers.</p>')
    Validate.is_type(i, int)
    Debug.random_number(i, integer=True)
    
    """Date and time debugging"""
    p = Page(b)
    Label(p, label='<p>Debugging for date and time inputs.</p>')
    Input(p, input_type='date')
    Input(p, input_type='datetime-local')
    Input(p, input_type='month')
    Input(p, input_type='time')
    Input(p, input_type='week')

    """Range debugging"""
    p = Page(b)
    Range(p, label='<p>Debugging for range input.</p>')

    """Choice question debugging"""
    p = Page(b)
    Label(p, label='<p>Debugging for choice questions.</p>')
    Check(p, choices=['Red','Green','Blue'])
    Check(p, choices=['World','Moon','Sun'], multiple=True)
    Select(p, choices=['1','2','3'])
    Select(p, choices=['Canada','United States','Mexico'], multiple=True)

    """Custom debugging functions"""
    p = Page(b)
    i = Input(p, label='<p>Enter "hello world" to continue.</p>')
    Validate.match(i, 'hello world')
    Debug.send_keys(i, 'hello world')
    
    check = Check(p)
    Choice(check, label='Correct', value=1)
    Choice(check, label='Incorrect', value=0)
    Validate.correct_choices(check)
    Debug.click_choices(check, check.choices[0])

    i = Input(p, label='<p>Enter "goodbye moon" to continue.</p>')
    Validate.match(i, 'goodbye moon')
    Debug.send_goodbye_moon(i)

    return b

@Debug.register
def send_goodbye_moon(inpt, driver):
    input_from_driver = inpt.input_from_driver(driver)
    input_from_driver.clear()
    input_from_driver.send_keys('goodbye moon')

def ComprehensionCheck(root=None):
    instructions, checks = [], []

    p = Page()
    Label(p, label='<p>Instructions page 1.</p>')
    instructions.append(p)

    p = Page()
    Label(p, label='<p>Instrucitons page 2.</p>')
    instructions.append(p)

    p = Page()
    s = Select(p, label='<p>Select the correct answer.</p>')
    Option(s, label='Incorrect', value=0)
    Option(s, label='Correct', value=1)
    checks.append(p)

    p = Page()
    i = Input(p, label='<p>Enter "the correct answer".</p>')
    Submit.match(i, 'the correct answer')
    checks.append(p)

    b = comprehension_check(instructions=instructions, checks=checks, attempts=2)
    Navigate.End(b)
    return b