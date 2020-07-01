"""# Selenium webdrivers"""

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