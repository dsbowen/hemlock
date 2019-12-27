"""Debug functions

Page:
1. forward navigation
2. back navigation
3. navigate randomly

Textarea and text Input:

Date and time input:

Default input debugger

ChoiceQuestion:
???

Page:
1. click_forward
2. click_back
3. random_navigate
"""

from hemlock.app import Settings
from hemlock.database import Debug

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from datetime import datetime, timedelta
from random import choice, randint, random, shuffle
from string import ascii_letters, digits
from time import sleep

"""Page debugging"""
@Debug.register
def forward(page, driver):
    driver.find_element_by_id('forward-btn').click()

@Debug.register
def back(page, driver):
    driver.find_element_by_id('back-btn').click()

@Debug.register
def navigate(page, driver, p_forward=.8, p_back=.1, sleep_time=3):
    """Navigate randomly

    This method randomly navigates forward or backward, or refreshes the 
    page.
    """
    forward_exists = back_exists = True
    if random() < p_forward:
        try:
            return forward(page, driver)
        except:
            forward_exists = False
    if random() < p_back / (1 - p_forward):
        try:
            return back(page, driver)
        except:
            back_exists = False
    if not (forward_exists or back_exists):
        sleep(sleep_time)
    driver.refresh()

def debug_fn(page, driver):
    """Run the question debug functions in random order"""
    order = list(range(len(page.questions)))
    shuffle(order)
    [page.questions[i]._debug(driver) for i in order]

@Settings.register('Page')
def settings():
    return {'debug_functions': [debug_fn, navigate]}

"""Textarea and text Input debugging"""
@Debug.register
def send_keys(question, driver, keys):
    """Send keys method

    This debugger sends the specified keys or list or keys to the textarea 
    or input.
    """
    try:
        inpt = question.textarea_from_driver(driver)
    except:
        inpt = question.input_from_driver(driver)
    inpt.clear()
    if isinstance(keys, list):
        [inpt.send_keys(key) for key in keys]
    else:
        inpt.send_keys(keys)

@Debug.register
def random_str(question, driver, magnitude=2, p_whitespace=.2):
    """Random string

    This debugger sends a random string to the textarea. `magnitude` is the 
    maximum magnitude of the length of the string. `p_whitespace` is the 
    probability of sending a whitespace character.
    """
    chars = ascii_letters + digits
    chars = list(chars) + [' '] * int(p_whitespace*len(chars))
    length = int(random() * 10**randint(1,magnitude))
    send_keys(
        question, driver, ''.join([choice(chars) for i in range(length)])
    )

@Debug.register
def random_number(question, driver, *args, **kwargs):
    send_keys(question, driver, str(gen_number(*args, **kwargs)))

def gen_number(
        integer=False, magnitude_lb=0, magnitude_ub=10, p_negative=.1, 
        max_decimals=5
    ):
    """Generate a random number

    `magnitude_lb` and `magnitude_ub` specify the lower and upper bound on 
    the mangitude of the number. 
    `p_negative` is the probability of generating a random number. 
    `max_decimals` is the maximum number of decimals to which the number 
    can be rounded.
    """
    num = random() * 10**randint(magnitude_lb, magnitude_ub)
    if random() < p_negative:
        num = -num
    if integer:
        return int(num)
    return round(num, randint(0, max_decimals))

@Debug.register
def random_keys(question, driver, p_str=.5, p_int=.25):
    """Send random keys

    This method sends random keys to a textarea or input. 
    
    With probability `p_skip`, this method skips the question without sending keys.
    With probability `p_str`, this method sends a random string.
    With probability `p_int`, this method sends an integer.
    Otherwise, it sends a floating point number.
    """
    if random() < p_str:
        return random_str(question, driver)
    integer = random() < p_int / (1-p_str)
    random_number(question, driver, integer=integer)

def default_textarea_debug(question, driver, p_skip=.1):
    """Skip or send random string"""
    if random() < p_skip:
        return
    random_str(question, driver)
    
@Settings.register('Textarea')
def settings():
    return {'debug_functions': default_textarea_debug}

"""Date and time input"""
@Debug.register
def random_date(question, driver, **kwargs):
    dt = gen_datetime(**kwargs)
    send_keys(question, driver, dt.strftime('%m%d%Y'))

@Debug.register
def random_datetime(question, driver, **kwargs):
    dt = gen_datetime(**kwargs)
    date = dt.strftime('%m%d%Y')
    time = dt.strftime('%I%M%p')
    send_keys(question, driver, [date, Keys.TAB, time])

@Debug.register
def random_month(question, driver, **kwargs):
    dt = gen_datetime(**kwargs)
    month = dt.strftime('%B')
    send_keys(question, driver, [month, Keys.TAB, str(dt.year)])

@Debug.register
def random_time(question, driver, **kwargs):
    dt = gen_datetime(**kwargs)
    send_keys(question, driver, dt.strftime('%I%M%p'))

@Debug.register
def random_week(question, driver, **kwargs):
    dt = gen_datetime(**kwargs)
    send_keys(question, driver, dt.strftime('%U%Y'))

def gen_datetime(p_future=.5, **kwargs):
    """Randomly generate datetime

    This method randomly generates a datetime object by subtracting a 
    timedelta from the current datetime. The timedelta's seconds are 
    determined by the random number generator specified above.
    """
    kwargs['magnitude_lb'] = kwargs.get('magnitude_lb') or 2
    kwargs['p_negative'] = p_future or kwargs.get('p_negative')
    seconds = gen_number(**kwargs)
    return datetime.now() - timedelta(seconds=seconds)

"""Default input debugger"""
input_debug_fn_map = {
    'date': random_date,
    'datetime-local': random_datetime,
    'month': random_month,
    'time': random_time,
    'week': random_week,
}

def default_input_debug(question, driver, p_skip=.1):
    if random() < p_skip:
        return
    debug_fn = input_debug_fn_map.get(question.input_type) or random_keys
    debug_fn(question, driver)

@Settings.register('Input')
def settings():
    return {
        'debug_functions': default_input_debug
    }

"""Range debugger"""
@Debug.register
def drag_range(question, driver, xoffset=None):
    """Drag the range slider to xoffset"""
    xoffset = xoffset or randint(-300,300)
    inpt = question.input_from_driver(driver)
    ActionChains(driver).drag_and_drop_by_offset(inpt, xoffset, 0).perform()

@Settings.register('Range')
def settings():
    return {'debug_functions': drag_range}

"""Choice question debugger"""
@Debug.register
def click_choices(question, driver, *choices):
    """Click on input choices

    Note: the try/except is due to an open issue, possibly due to dragula. 
    See more here https://github.com/bevacqua/dragula/issues/569.
    """
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL)
    for choice in choices:
        actions.click(choice.input_from_driver(driver))
    try:
        actions.key_up(Keys.CONTROL).perform()
    except:
        pass

def default_choice_question_debug(question, driver, p_skip=.1):
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
    click_choices(question, driver, *to_click)

@Settings.register('ChoiceQuestion')
def settings():
    return {
        'debug_functions': default_choice_question_debug
    }