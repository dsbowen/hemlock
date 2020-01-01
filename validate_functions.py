"""Validate and Debug functions"""

import navigate_functions

from hemlock import *

from random import choice, random

@Navigate.register
def ValidateFunctions(origin=None):
    b = Branch()
    Navigate.NavigateFunctions(b)

    """Require and type validation"""
    p = Page(b, name='Require and type validation')

    i = Input(
        p, 
        label='<p>Enter anything you like (but you must enter something).</p>'
    )
    Validate.require(i)

    i = Input(p, label='<p>Enter any number.</p>')
    Validate.is_type(i, float)
    Debug.random_number(i, p_exec=.9)

    i = Input(p, label='<p>Enter an integer.</p>')
    Validate.is_type(i, int)
    Debug.random_number(i, integer=True, p_exec=.9)

    """Set validation"""
    p = Page(b, name='Set validation')

    i = Input(p, label='<p>Enter 1, 2, or 3.</p>')
    Validate.is_in(i, ['1', '2', '3'])
    Debug.send_keys(i, 1, p_exec=.9)

    i = Input(p, label='<p>Do not enter 1, 2, or 3.</p>')
    Validate.is_not_in(i, ['1','2','3'])

    """Range validation"""
    p = Page(b, name='Range valiation')

    i = Input(p, label='<p>Enter a number less than 100.</p>')
    Validate.max_val(i, 100, resp_type=float)
    Debug.send_keys(i, 50, p_exec=.9)

    i = Input(p, label='<p>Enter a number greater than 0.</p>')
    Validate.min_val(i, 0, resp_type=float)
    Debug.send_keys(i, 50, p_exec=.9)

    i = Input(p, label='<p>Enter a number between 0 and 100.</p>')
    Validate.range_val(i, min=0, max=100, resp_type=float)
    Debug.send_keys(i, 50, p_exec=.9)

    """Length"""
    p = Page(b, name='Length validation')

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
    p = Page(b, name='Number of choices validation')

    s = Select(
        p,
        label='<p>Select at most 2 choices.</p>',
        multiple=True,
        choices=['Red','Green','Blue']
    )
    Validate.max_len(s, 2)
    Debug.clear_choices(s, p_exec=.9)

    c = Check(
        p,
        label='<p>Select at least 1 choice.</p>',
        multiple=True,
        choices=[1,2,3]
    )
    Validate.min_len(c, 1)
    Debug.click_choices(c, c.choices[0], p_exec=.9)


    s = Select(
        p,
        label='<p>Select between 2 and 3 choices.</p>',
        multiple=True,
        choices=['World','Moon','Star']
    )
    Validate.range_len(s, min=2, max=3)
    Debug.click_choices(s, *list(s.choices), p_exec=.9)

    c = Check(
        p,
        label='<p>Select exactly 2 choices.</p>',
        multiple=True,
        choices=['Hello','Hola','Bonjour']
    )
    Validate.exact_len(c, 2)
    Debug.click_choices(c, *c.choices[:2], p_exec=.9)

    """Number of words validation"""
    p = Page(b, name='Number of words validation')

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
    p = Page(b, name='Decimal validation')

    i = Input(p, label='<p>Enter a number with at most 3 decimals.</p>')
    Validate.max_decimals(i, 3)
    Debug.send_keys(i, '1.12', p_exec=.9)

    i = Input(p, label='<p>Enter a number with at least 1 decimal.</p>')
    Validate.min_decimals(i, 1)
    Debug.send_keys(i, '1.12', p_exec=.9)

    i = Input(p, label='<p>Enter a number with between 0 and 3 decimals.</p>')
    Validate.range_decimals(i, min=0, max=3)
    Debug.send_keys(i, '1.12', p_exec=.9)

    i = Input(
        p,
        label='<p>Enter a number with exactly 2 decimals.</p>',
        prepend='$'
    )
    Validate.exact_decimals(i, 2)
    Debug.send_keys(i, '1.12', p_exec=.9)

    """Regex validation"""
    p = Page(b, name='Regex validation')
    i = Input(p, label='<p>Who is the best 2020 presidential candidate?</p>')
    Validate.match(i, pattern='Andrew Yang')
    Debug.send_keys(i, 'Andrew Yang', p_exec=.9)

    """Choice validation"""
    p = Page(b, name='Choice validation')

    s = Select(p, label='<p>Select the correct answer.</p>')
    Option(s, label='Incorrect', value=0)
    Option(s, label='Correct', value=1)
    Validate.correct_choices(s)
    Debug.click_choices(s, s.choices[1], p_exec=.9)

    c = Check(p, label='<p>Select one of the correct answers.</p>')
    Choice(c, label='Correct 1', value=1)
    Choice(c, label='Correct 2', value=1)
    Choice(c, label='Incorrect', value=0)
    Validate.correct_choices(c)
    Debug.click_choices(c, c.choices[0], p_exec=.9)

    s = Select(
        p, 
        label='<p>Select all of the correct answers.</p>',
        multiple=True
    )
    Option(s, label='Correct 1', value=1)
    Option(s, label='Correct 2', value=1)
    Option(s, label='Incorrect', value=0)
    Validate.correct_choices(s)
    Debug.click_choices(s, *s.choices[:2], p_exec=.9)

    """Question validation"""
    p = Page(b, name='Custom question validation')
    password = Input(p, label='<p>Enter your password.</p>')
    confirm = Input(p, label='<p>Confirm password.</p>')
    Validate.confirm_password1(confirm, password)
    Debug.send_keys(password, 'password', p_exec=.9)
    Debug.send_keys(confirm, 'password', p_exec=.9)

    """Page validation"""
    p = Page(b, name='Custom page validation')
    password = Input(p, label='<p>Enter your password.</p>')
    confirm = Input(p, label='<p>Confirm password.</p>')
    Validate.confirm_password2(p, password, confirm)
    Debug.send_keys(password, 'password', p_exec=.9)
    Debug.send_keys(confirm, 'password', p_exec=.9)

    """Custom debugging"""
    p = Page(b, name='Custom debugging')
    i = Input(p, label='<p>Enter 1, 2, or 3</p>')
    Validate.is_in(i, ['1','2','3'])
    Debug.send_1_3(i, p_exec=.9)

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
def send_1_3(i, driver, p_exec=1):
    """Send a random integer between 1 and 3 (inclusive)"""
    if random() > p_exec:
        return
    inpt = i.input_from_driver(driver)
    inpt.clear()
    inpt.send_keys(choice(['1','2','3']))