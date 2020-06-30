"""# Debug functions


"""

from ..app import settings
from ..models import Debug
from ..qpolymorphs import Check
from .utils import gen_datetime, gen_number

from datetime_selenium import send_datetime as send_datetime_
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from datetime import datetime, timedelta
from random import choice, randint, random, shuffle
from string import ascii_letters, digits
from time import sleep

# Page debugging
@Debug.register
def forward(driver, page):
    """
    Click the forward button.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    page : hemlock.Page
    """
    driver.find_element_by_id('forward-btn').click()

@Debug.register
def back(driver, page):
    """
    Click the back button.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    page : hemlock.Page
    """
    driver.find_element_by_id('back-btn').click()

# Textarea and text input debugging

@Debug.register
def send_keys(driver, question, *keys, p_num=.5):
    """
    Send the specified keys to the `<textarea>` or `<input>`.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.Question

    \*keys : 
        Keys to send to the textarea or input. If empty, keys are randomly 
        selected.

    p_num : float, default=.5
        Probability of sending a random number if keys are not specified (as 
        opposed to a random string).
    """
    try:
        inpt = question.textarea_from_driver(driver)
    except:
        inpt = question.input_from_driver(driver)
    inpt.clear()
    if keys:
        [inpt.send_keys(key) for key in keys]
    elif random() < p_num:
        random_number(driver, question)
    else:
        random_string(driver, question)

@Debug.register
def random_str(driver, question, magnitude=2, p_whitespace=.2):
    """
    Send a random string to the textarea.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.Question

    magnitude : int, default=2
        Maximum magnitude of the length of the string. e.g. the default
        magnitude of 2 means that the maximum length is 10^2=100 characters.

    p_whitespace : float, default=.2
        Frequency with which whitespace characters appear in the string.
    """
    chars = ascii_letters + digits
    chars = list(chars) + [' '] * int(p_whitespace*len(chars))
    length = int(random() * 10**randint(1,magnitude))
    keys = ''.join([choice(chars) for i in range(length)])
    send_keys(driver, question, keys)

@Debug.register
def random_number(driver, question, *args, **kwargs):
    """
    Send a random number to the textarea or input.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.Question

    magn_lb : int, default=0
        Lower bound for the magnitude of the number.

    mag_ub : int, default=10
        Upper bound for the magnitude of the number.

    max_decimals : int, default=5
        Maximum number of decimals to which the number can be rounded.

    p_int : float, default=.5
        Probability that the number is an integer.

    p_neg : float, default=.1
        Probability that the number is negative.
    """
    send_keys(driver, question, str(gen_number(*args, **kwargs)))

# Date and time input
@Debug.register
def send_datetime(driver, question, datetime_=None):
    """
    Send a `datetime.datetime` object to an input. Inputs should be of type
    'date', 'datetime-local', 'month', 'time', or 'week',

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.Question

    datetime_ : datetime.datetime or None, default=None
        The datetime object to send. If `None`, a date and time are chosen
        randomly.
    """
    datetime_ = datetime_ or gen_datetime()
    send_datetime_(question.input_from_driver(driver), date_time_)

"""Range debugger"""
# HERE
@Debug.register
def drag_range(driver, question, xoffset=None):
    """Drag the range slider to xoffset"""
    xoffset = xoffset or randint(-300,300)
    inpt = question.input_from_driver(driver)
    ActionChains(driver).drag_and_drop_by_offset(inpt, xoffset, 0).perform()

@Settings.register('Range')
def settings():
    return {'debug_functions': drag_range}

"""Choice question debugger"""
@Debug.register
def click_choices(driver, question, *choices, p_exec=1):
    """Click on input choices"""
    if random() > p_exec:
        return
    if question.multiple:
        clear_choices(driver, question)
    if isinstance(question, Check):
        return [c.label_from_driver(driver).click() for c in choices]
    return [c.input_from_driver(driver).click() for c in choices]

@Debug.register
def clear_choices(driver, question, p_exec=1):
    if random() > p_exec or not question.choices:
        return
    if not question.multiple:
        print("Warning: Only multiple choice questions cannot be cleared")
        return
    for c in question.choices:
        if c.input_from_driver(driver).get_attribute('checked'):
            if isinstance(question, Check):
                c.label_from_driver(driver).click()
            else:
                c.input_from_driver(driver).click()
                

def default_choice_question_debug(driver, question, p_skip=.1):
    """Default choice question debugging function

    This method randomly selects choices to click on. The number of choices 
    to click on is a random number from 0 to len(question.choices).
    """
    if random() < p_skip:
        return
    choices = question.choices
    order = list(range(len(choices)))
    shuffle(order)
    num_clicks = randint(0, len(choices))
    to_click = [question.choices[i] for i in order[0:num_clicks]]
    click_choices(driver, question, *to_click)

@Settings.register('ChoiceQuestion')
def settings():
    return {
        'debug_functions': default_choice_question_debug
    }