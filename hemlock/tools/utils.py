"""# Utilities"""

from cssutils import parseStyle
from flask import render_template, url_for as try_url_for
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

import os

def chromedriver(headless=False):
    """
    Parameters
    ----------
    headless : bool, default=False
        Indicates whether to run Chrome in headless mode.

    Returns
    -------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    Notes
    -----
    Chromedriver must be headless in production. When the application is in 
    production, this method sets `headless` to `True` regardless of the 
    parameter you pass.

    Examples
    --------
    ```python
    from hemlock.tools import chromedriver

    driver = chromedriver()
    ```
    """
    options = Options()
    url_root = os.environ.get('URL_ROOT')
    if headless or (url_root and 'localhost' not in url_root):
        options._arguments = ['--disable-gpu', '--no-sandbox', '--headless']
    else: 
        options._arguments = ['--disable-gpu', '--no-sandbox']
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN', '')
    driver_path = os.environ.get('CHROMEDRIVER_PATH')
    return (
        Chrome(driver_path, options=options) if driver_path 
        else Chrome(options=options)
    )

def get_data(dataframe='data'):
    """
    Parameters
    ----------
    dataframe : str, default='data'
        Name of the dataframe to get; `'data'` or `'meta'`.

    Returns
    -------
    data : dict
        Maps variable names to list of entries. May not include data from
        participants who are in progress.

    Examples
    --------
    ```python
    from hemlock import Branch, Page, Participant, push_app_context
    from hemlock.tools import get_data

    def start():
    \    return Branch(Page())

    push_app_context()

    Participant.gen_test_participant(start).completed = True
    get_data()
    ```

    Out:

    ```
    {'ID': [1],
    'EndTime': [datetime.datetime(2020, 7, 6, 17, 11, 0, 245032)],
    'StartTime': [datetime.datetime(2020, 7, 6, 17, 11, 0, 245032)],
    'Status': ['Completed']}
    ```
    """
    from ..models.private import DataStore
    return dict(getattr(DataStore.query.first(), dataframe))

def show_on_event(
        target, condition, value, init_hidden=True, *args,  **kwargs
    ):
    """
    Show the target question when a condition is met.

    Parameters
    ----------
    target : hemlock.Question
        The question which will be shown when the condition is met.

    condition : hemlock.Question
        The question whose value determines whether the target is shown.

    value : str or hemlock.Choice
        1. If the condition is an input, the target is shown when the input 
        value matches this value.
        2. If the condition has choices, the target is shown when the choice
        with this value is checked.

    init_hidden : bool, defualt=True
        Indicates that the initial state of the target should be hidden.

    regex : bool, default=False
        Indicates that the target will be shown if input value matches the 
        string as a regular expression.

    event : str or None, default=None
        Type of event which toggles the target display. If `None`, this 
        function infers the type of event based on inputs.

    duration : str or int, default=400
        Show/hide event duration in milliseconds.

    Examples
    --------
    ```python
    from hemlock import Page, Check, Input, Label, push_app_context
    from hemlock.tools import show_on_event

    app = push_app_context()

    race = Check(
    \    '<p>Indicate your race.</p>', 
    \    ['White', 'Black', 'Other'], 
    \    multiple=True
    )
    specify = Input('<p>Please specify.</p>')
    show_on_event(specify, race, 'Other')
    Page(race, specify).preview()
    ```

    ```python
    name = Input("<p>What's your name?</p>")
    greet = Label("<p>Hello, World!</p>")
    show_on_event(greet, name, '(w|W)orld', regex=True, duration=400)
    Page(name, greet).preview()
    ```
    """
    from ..models import Question
    from ..qpolymorphs import Choice, Option

    # NOTE I want to extend this to show choices and options as well
    # but the code below isn't working right now

    # assert (
    #     isinstance(target, (Question, Choice, Option)), 
    #     'target must be a Question, Choice, or Option'
    # )
    # if isinstance(target, Question):
    #     # form-group
    #     target_id = target.model_id+'-fg'
    # elif isinstance(target, Choice):
    #     # custom-conctrol
    #     target_id = target.model_id+'-cc'
    # else:
    #     # option
    #     target_id = target.model_id
    assert isinstance(target, Question), 'target must be a Question'
    if init_hidden:
        if 'style' not in target.form_group_attrs:
            target.form_group_attrs['style'] = {}
        target.form_group_attrs['style']['display'] = 'none'
    target.js.append(
        _show_on_event_js(target, condition, value, *args, **kwargs)
    )
    return target

def _show_on_event_js(
        target, condition, value, regex=False, duration=400, event=None, 
    ):
    from ..models import ChoiceQuestion
    from ..qpolymorphs import Binary, Check, Select

    def get_event_value(condition, value):
        if isinstance(condition, ChoiceQuestion):
            event = 'change' # listen for change event
            for choice in condition.choices:
                if choice.value == value:
                    value = choice.key
                    break
        else:
            event = 'input' # listen for input event
        return event, value

    event, value = get_event_value(condition, value)
    choice = option = False # value is neither a radio, check box, or option
    if isinstance(condition, (Binary, Check)):
        # value corresponds to radio or check box
        choice, option = True, False
    elif isinstance(condition, Select):
        # value corresponds to option
        choice, option = False, True        
    return render_template(
        'hemlock/show-on-event.html', 
        target=target, 
        condition=condition,
        choice=choice,
        option=option,
        value=value, 
        regex=regex, 
        event=event, 
        duration=duration
    )

def url_for(*args, **kwargs):
    """
    Attempt to return `flask.url_for(*args, **kwargs)`. However, this method 
    does not exit the program when getting a url outside a request context; 
    e.g. when debugging in a shell or notebook.

    Parameters
    ----------
    \*args, \*\*kwargs :
        Arguments and keyword arguments will be passed to `flask.url_for`.

    Returns
    -------
    url : str
        Output of `flask.url_for` if possible; otherwise `'URL_UNAVAILABLE'`.
    """
    try:
        return try_url_for(*args, **kwargs)
    except:
        return 'URL_UNAVAILABLE'