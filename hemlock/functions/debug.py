"""# Debug functions

Debug functions tell the AI participant what to do during debugging. They 
generally take a selenium webdriver as their first argument and a page or 
question as their second argument.

Notes
-----
The following examples open a webdriver. After running the examples, close the
driver with `driver.close()`.

By default, the last debug function of a page navigates. To remove this, run
`page.debug.pop()`.
"""

from ..app import settings
from ..models import Debug
from .utils import random_datetime, random_num, random_str

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_tools import (
    drag_range as drag_range_, send_datetime as send_datetime_
)

import math
from datetime import datetime, timedelta
from random import randint, random, randrange, shuffle

from time import sleep

def _is_displayed(element, max_wait=1, wait_interval=1):
    """
    Parameters
    ----------
    element : selenium.webdriver.remote.webelement.WebElement
        Checks if this element is displayed.

    max_wait : float, default=1
        Maximum number of seconds to wait for element to be displayed.

    wait_interval : float, default=1
        Interval in between checking to see if element is displayed.

    Returns
    -------
    is_displayed : bool
        Indicates that the web element is displayed.
    """
    for _ in range(0, max_wait, wait_interval):
        if element.is_displayed():
            return True
        sleep(wait_interval)
    return False

# Page debugging
@Debug.register
def forward(driver, page, max_wait=30, wait_interval=3):
    """
    Click the forward button.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    page : hemlock.Page

    Examples
    --------
    ```python
    from hemlock import Debug as D, Page, push_app_context
    from hemlock.tools import chromedriver

    app = push_app_context()

    driver = chromedriver()

    p = Page(debug=[D.debug_questions(), D.forward()])
    p.preview(driver)._debug(driver)
    ```
    """
    forward_btn = driver.find_element_by_id('forward-btn')
    if _is_displayed(forward_btn, max_wait, wait_interval):
        forward_btn.click()
    else:
        raise TimeoutError('Forward button not displayed')

@Debug.register
def back(driver, page, max_wait=30, wait_interval=1):
    """
    Click the back button.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    page : hemlock.Page

    Examples
    --------
    ```python
    from hemlock import Debug as D, Page, push_app_context
    from hemlock.tools import chromedriver

    app = push_app_context()

    driver = chromedriver()

    p = Page(debug=[D.debug_questions(), D.back()])
    p.preview(driver)._debug(driver)
    ```
    """
    back_btn = driver.find_element_by_id('back-btn')
    if _is_displayed(back_btn, max_wait, wait_interval):
        back_btn.click()
    else:
        raise TimeoutError('Back button not displayed')

# Textarea and input debugging

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

    Notes
    -----
    This debug function is skipped if the question is not displayed.

    Examples
    --------
    ```python
    from hemlock import Debug as D, Input, Page, push_app_context
    from hemlock.tools import chromedriver

    app = push_app_context()

    driver = chromedriver()

    p = Page(Input(debug=D.send_keys('hello world')))
    p.preview(driver)._debug(driver)
    ```
    """
    def random_keys():
        html_datetime_types = (
            'date', 'datetime-local', 'month', 'time', 'week'
        )
        type_ = inpt.get_attribute('type')
        if inpt.tag_name == 'textarea' or not type_ or type_ == 'text':
            if random() < p_num:
                random_num(inpt)
            else:
                random_str(inpt)
        elif type_ == 'number':
            random_num(inpt)
        elif type_ in html_datetime_types:
            random_datetime(inpt)

    inpt = question.input_from_driver(driver)
    if _is_displayed(inpt):
        inpt.clear()
        if keys:
            [inpt.send_keys(key) for key in keys]
        else:
            random_keys()

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

    Notes
    -----
    This debug function is skipped if the question is not displayed.

    Examples
    --------
    ```python
    from hemlock import Debug as D, Input, Page, push_app_context
    from hemlock.tools import chromedriver

    from datetime import datetime

    app = push_app_context()

    driver = chromedriver()

    p = Page(Input(type='date', debug=D.send_datetime(datetime.utcnow())))
    p.preview(driver)._debug(driver)
    ```
    """
    inpt = question.input_from_driver(driver)
    if _is_displayed(inpt):
        inpt.clear()
        random_datetime(inpt)

# Range debugger

@Debug.register
def drag_range(driver, range_, target=None, tol=0, max_iter=10):
    """
    Drag a range slider to specified target value.
    
    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    range_ : hemlock.Range

    target : float or None, default=None
        Target value to which the slider should be dragged. If `None`, a
        random target value will be chosen.

    tol : float, default=0
        Tolerance for error if the slider cannot be dragged to the exact
        target.

    max_iter : int, default=10
        Maximum number of iterations for the slider to reach the target.

    Notes
    -----
    This debug function is skipped if the question is not displayed.

    Examples
    --------
    ```python
    from hemlock import Debug as D, Page, Range, push_app_context
    from hemlock.tools import chromedriver

    app = push_app_context()

    driver = chromedriver()

    p = Page(Range(debug=D.drag_range(80)))
    p.preview(driver)._debug(driver)
    ```
    """
    if target is None:
        target = randint(range_.min, range_.max)
        target = round(target / range_.step) * range_.step
    inpt = range_.input_from_driver(driver)
    if _is_displayed(inpt):
        drag_range_(
            driver, inpt, target,
            horizontal=True, # all sliders are horizontal for now
            tol=tol,
            max_iter=max_iter
        )

# Choice question debugger

@Debug.register
def click_choices(driver, question, *values, if_selected=None, max_clicks=5):
    """
    Click on choices or options.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.ChoiceQuestion
    
    \*values : 
        Values of the choices on which to click. If no choices are specified, 
        the debugger will click on random choices.

    if_selected : bool or None, default=None
        Indicates that the choices will be clicked only if they are already 
        selected. If `False` the choices will be clicked only if they are not 
        already selected. If `None` the choices will be clicked whether or 
        not they are selected.

    Notes
    -----
    Will not attempt to click choices or options which are not displayed.

    Examples
    --------
    ```python
    from hemlock import Binary, Debug as D, Page, push_app_context
    from hemlock.tools import chromedriver

    app = push_app_context()

    driver = chromedriver()

    p = Page(
    \    Binary(
    \        '<p>Click "Yes".</p>', 
    \        debug=D.click_choices('Yes')
    \    )
    )
    p.preview(driver)._debug(driver)
    """
    def choose_values():
        order = list(range(len(question.choices)))
        shuffle(order)
        n_values = max(randint(0, len(question.choices)), max_clicks)
        return [question.choices[i].value for i in order[:n_values]]

    values = values if values else choose_values()
    for c in question.choices:
        if c.value in values and c.is_displayed(driver):
            c.click(driver, if_selected=if_selected)

@Debug.register
def clear_choices(driver, question):
    """
    Clear selected choices.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.ChoiceQuestion

    Notes
    -----
    Intended only for questions in which multiple choices may be selected.

    Examples
    --------
    ```python
    from hemlock import Check, Debug as D, Page, push_app_context
    from hemlock.tools import chromedriver

    app = push_app_context()

    driver = chromedriver()

    p = Page(
    \    Check(
    \        "<p>Which ice cream flavors do you like?</p>",
    \        ['Chocolate', 'Vanilla', 'Strawberry'],
    \        default='Chocolate', 
    \        multiple=True,
    \        debug=D.clear_choices()
    \    )
    )
    p.preview(driver)._debug(driver)
    ```
    """
    if not question.choices:
        return
    if not question.multiple:
        print("Warning: Only multiple choice questions cannot be cleared")
        return
    for c in question.choices:
        if c.is_displayed(driver):
            c.click(driver, if_selected=True)