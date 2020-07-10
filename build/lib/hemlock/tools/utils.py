"""# Utilities"""

from flask import url_for as try_url_for
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