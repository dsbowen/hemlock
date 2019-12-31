"""Validate functions"""

from hemlock import *

from random import random

@route('/survey')
def ValidateFunctions(origin=None):
    b = Branch()
    Navigate.End(b)

    """Require and type validation"""
    p = Page(b)

    i = Input(
        p, 
        label='<p>Enter anything you like (but you must enter something).</p>'
    )
    Validate.require(i)

    i = Input(p, label='<p>Enter an integer.</p>')
    Validate.is_type(i, int)

    """Set validation"""
    p = Page(b)

    i = Input(p, label='<p>Enter 1, 2, or 3.</p>')
    Validate.is_in(i, ['1', '2', '3'])

    i = Input(p, label='<p>Do not enter 1, 2, or 3.</p>')
    Validate.is_not_in(i, ['1','2','3'])

    """Range validation"""
    p = Page(b)

    i = Input(p, label='<p>Enter a number less than 100.</p>')
    Validate.max_val(i, 100, resp_type=float)
    Debug.send_keys(i, 50, p_exec=.8)

    i = Input(p, label='<p>Enter a number greater than 0.</p>')
    Validate.min_val(i, 0, resp_type=float)
    Debug.send_keys(i, 50, p_exec=.8)

    i = Input(p, label='<p>Enter a number between 0 and 100.</p>')
    Validate.range_val(i, min=0, max=100, resp_type=float)
    Debug.send_keys(i, 50, p_exec=.8)

    """Length"""
    p = Page(b)

    t = Textarea(p, label='<p>Enter a maximum of 10 characters.</p>')
    Validate.max_len(t, 10)
    Debug.send_keys(t, '1234567', p_exec=.9)

    t = Textarea(p, label='<p>Enter at least 5 characters.</p>')
    Validate.min_len(t, 5)
    Debug.send_keys(t, '1234567', p_exec=.9)

    t = Textarea(p, label='<p>Enter between 5 and 10 characters.</p>')
    Validate.range_len(t, min=5, max=10)
    Debug.send_keys(t, '1234567', p_exec=.9)

    t = Textarea(p, label='<p>Enter exactly 7 characters.</p>')
    Validate.exact_len(t, 7)
    Debug.send_keys(t, '1234567', p_exec=.9)

    """Number of choices"""
    p = Page(b)

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
        choices=[1,2,3]
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
        choices=['Hello','Hola','Bonjour']
    )
    Validate.exact_len(c, 2)

    """Number of words validation"""
    p = Page(b)

    t = Textarea(p, label='<p>Enter at most 3 words.</p>')
    Validate.max_words(t, 3)
    Debug.send_keys(t, 'hello world', p_exec=.9)

    t = Textarea(p, label='<p>Enter at least 1 word.</p>')
    Validate.min_words(t, 1)
    Debug.send_keys(t, 'hello world', p_exec=.9)

    t = Textarea(p, label='<p>Enter between 1 and 3 words.</p>')
    Validate.range_words(t, min=1, max=3)
    Debug.send_keys(t, 'hello world', p_exec=.9)

    t = Textarea(p, label='<p>Enter exactly 2 words.</p>')
    Validate.exact_words(t, 2)
    Debug.send_keys(t, 'hello world', p_exec=.9)

    """Decimal validation"""
    p = Page(b)

    i = Input(p, label='<p>Enter a number with at most 3 decimals.</p>')
    Validate.max_decimals(i, 3)
    Debug.send_keys(i, 1.12, p_exec=.9)

    i = Input(p, label='<p>Enter a number with at least 1 decimal.</p>')
    Validate.min_decimals(i, 1)
    Debug.send_keys(i, 1.12, p_exec=.9)

    i = Input(p, label='<p>Enter a number with between 0 and 3 decimals.</p>')
    Validate.range_decimals(i, min=0, max=3)
    Debug.send_keys(i, 1.12, p_exec=.9)

    i = Input(
        p,
        label='<p>Enter a number with exactly 2 decimals.</p>',
        prepend='$'
    )
    Validate.exact_decimals(i, 2)
    Debug.send_keys(i, 1.12, p_exec=.9)

    """Regex validation"""
    p = Page(b)
    i = Input(p, label='<p>Enter a proper noun.</p>')
    Validate.match(i, pattern='([A-Z])\w+')
    Debug.send_keys(i, 'Andrew Yang', p_exec=.5)

    """Choice validation"""
    p = Page(b)

    s = Select(p, label='<p>Select the correct answer.</p>')
    Option(s, label='Incorrect', value=0)
    Option(s, label='Correct', value=1)
    Validate.correct_choices(s)

    c = Check(p, label='<p>Select one of the correct answers.</p>')
    Choice(c, label='Correct 1', value=1)
    Choice(c, label='Correct 2', value=1)
    Choice(c, label='Incorrect', value=0)
    Validate.correct_choices(c)

    s = Select(
        p, 
        label='<p>Select all of the correct answers.</p>',
        multiple=True
    )
    Option(s, label='Correct 1', value=1)
    Option(s, label='Correct 2', value=1)
    Option(s, label='Incorrect', value=0)
    Validate.correct_choices(s)

    """Question validation"""
    p = Page(b)
    password = Input(p, label='<p>Enter your password.</p>')
    confirm = Input(p, label='<p>Confirm password.</p>')
    Validate.confirm_password1(confirm, password)
    Debug.set_password(p)

    """Page validation"""
    p = Page(b)
    password = Input(p, label='<p>Enter your password.</p>')
    confirm = Input(p, label='<p>Confirm password.</p>')
    Validate.confirm_password2(p, password, confirm)
    Debug.set_password(p)

    return b

@Validate.register
def confirm_password1(confirm, password):
    if password.response != confirm.response:
        return '<p>Passwords must match.</p>'

@Validate.register
def confirm_password2(p, password, confirm):
    if password.response != confirm.response:
        return 'Passwords must match.'
        
@Debug.register
def set_password(page, driver):
    if random() > .8:
        return
    for q in page.questions:
        inpt = q.input_from_driver(driver)
        inpt.send_keys('password')

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

def Statics(root=None):
    b = Branch()

    """Video"""
    p = Page(b)
    vid = Vid.from_youtube('https://www.youtube.com/watch?v=LPYCtErvMyA')
    vid.parms['autoplay'] = 1
    Label(p, label=vid.render())

    """Image"""
    p = Page(b)
    img = Img(
        caption='Wanna See the Code?',
        alignment='center',
        src='https://imgs.xkcd.com/comics/wanna_see_the_code.png'
    )
    Label(p, label=img.render())

    """Images as choices"""
    p = Page(b)
    c = Check(p, label='<p>Pick your favorite.</p>')
    img = Img(src='https://imgs.xkcd.com/comics/halting_problem.png')
    Choice(c, label=img.render())
    img = Img(src='https://imgs.xkcd.com/comics/xkcde.png')
    Choice(c, label=img.render())
    img = Img(src='https://imgs.xkcd.com/comics/code_quality_2.png')
    Choice(c, label=img.render())

    return b

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