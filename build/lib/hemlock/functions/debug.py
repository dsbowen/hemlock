"""# Debug functions

Debug functions tell the AI participant what to do during debugging. They 
generally take a selenium webdriver as their first argument and a page or 
question as their second argument.

Notes
-----
The following examples open a webdriver. After running the examples, close the
driver with `driver.close()`.

By default, the last debug function of a page navigates. To remove this, run
`page.debug_functions.pop()`.
"""

from ..app import settings
from ..models import Debug
from .utils import gen_datetime, gen_number

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_tools import drag_range as drag_range_, send_datetime as send_datetime_

from datetime import datetime, timedelta
from random import choice, randint, random, randrange, shuffle
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

    Examples
    --------
    ```python
    from hemlock import Debug, Page, push_app_context
    from hemlock.tools import chromedriver

    push_app_context()

    driver = chromedriver()

    p = Page()
    # by default, last debug function navigates
    # so we want to remove this and replace it with forward
    p.debug_functions.pop()
    Debug.forward(p)
    p.preview(driver)._debug(driver)
    ```
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

    Examples
    --------
    ```python
    from hemlock import Debug, Page, push_app_context
    from hemlock.tools import chromedriver

    push_app_context()

    driver = chromedriver()

    p = Page(back=True)
    # by default, last debug function navigates
    # so we want to remove this and replace it with forward
    p.debug_functions.pop()
    Debug.back(p)
    p.preview(driver)._debug(driver)
    ```
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

    Examples
    --------
    ```python
    from hemlock import Debug, Input, Page, push_app_context
    from hemlock.tools import chromedriver

    push_app_context()

    driver = chromedriver()

    p = Page(Debug.send_keys(Input(), 'hello world'))
    p.preview(driver)._debug(driver)
    ```
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
        random_str(driver, question)

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

    Examples
    --------
    ```python
    from hemlock import Debug, Input, Page, push_app_context
    from hemlock.tools import chromedriver

    push_app_context()

    driver = chromedriver()

    p = Page(Debug.random_str(Input()))
    p.preview(driver)._debug(driver)
    ```
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

    Examples
    --------
    ```python
    from hemlock import Debug, Input, Page, push_app_context
    from hemlock.tools import chromedriver

    push_app_context()

    driver = chromedriver()

    p = Page(Debug.random_number(Input()))
    p.preview(driver)._debug(driver)
    ```
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

    Examples
    --------
    ```python
    from hemlock import Debug, Input, Page, push_app_context
    from hemlock.tools import chromedriver

    from datetime import datetime

    push_app_context()

    driver = chromedriver()

    p = Page(Debug.send_datetime(Input(input_type='date'), datetime.utcnow()))
    p.preview(driver)._debug(driver)
    ```
    """
    inpt = question.input_from_driver(driver)
    inpt.clear()
    datetime_ = datetime_ or gen_datetime()
    send_datetime_(inpt, datetime_)

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

    Examples
    --------
    ```python
    from hemlock import Debug, Page, Range, push_app_context
    from hemlock.tools import chromedriver

    push_app_context()

    driver = chromedriver()

    p = Page(Debug.drag_range(Range(), 80))
    p.preview(driver)._debug(driver)
    ```
    """
    if target is None:
        target = randrange(range_.min, range_.max, range_.step)
    drag_range_(
        driver, 
        range_.input_from_driver(driver),
        target,
        horizontal=True, # all sliders are horizontal for now
        tol=tol,
        max_iter=max_iter
    )

# Choice question debugger

@Debug.register
def click_choices(driver, question, *choices):
    """
    Click on choices or options.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.ChoiceQuestion
    
    \*choices : hemlock.Choice
        Choices on which to click. If no choices are specified, the 
        debugger will click on random choices.

    Examples
    --------
    ```python
    from hemlock import Check, Debug, Page, push_app_context
    from hemlock.tools import chromedriver

    push_app_context()

    driver = chromedriver()

    check = Check('<p>Check label</p>', ['Yes','No'])
    p = Page(Debug.click_choices(check, check.choices[0]))
    p.preview(driver)._debug(driver)
    ```
    """
    from ..qpolymorphs import Check
    if not choices:
        order = list(range(len(question.choices)))
        shuffle(order)
        n_clicks = randint(0, len(question.choices))
        choices = [question.choices[i] for i in order[0:n_clicks]]
    if question.multiple:
        clear_choices(driver, question)
    if isinstance(question, Check):
        # check question
        [c.label_from_driver(driver).click() for c in choices]
    else:
        # select question
        [c.input_from_driver(driver).click() for c in choices]

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
    from hemlock import Check, Debug, Page, push_app_context
    from hemlock.tools import chromedriver

    push_app_context()

    driver = chromedriver()

    check = Check('<p>Check label</p>', ['Yes','No'], multiple=True)
    check.default = list(check.choices)
    p = Page(Debug.clear_choices(check))
    p.preview(driver)._debug(driver)
    ```
    """
    from ..qpolymorphs import Check
    if not question.choices:
        return
    if not question.multiple:
        print("Warning: Only multiple choice questions cannot be cleared")
        return
    for c in question.choices:
        if c.input_from_driver(driver).get_attribute('checked'):
            if isinstance(question, Check):
                # check question
                c.label_from_driver(driver).click()
            else:
                # select question
                c.input_from_driver(driver).click()