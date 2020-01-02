"""Selenium webdrivers

Note: driver should be headless in the production environment and when 
creating a survey view.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def chromedriver(headless=False):
    options = Options()
    # use of selenium in production requires headless model
    if headless or 'localhost' not in os.environ.get('URL_ROOT'):
        options._arguments = ['--disable-gpu', '--no-sandbox', '--headless']
    else: 
        options._arguments = ['--disable-gpu', '--no-sandbox']
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    driver_path = os.environ.get('CHROMEDRIVER_PATH')
    if driver_path:
        return webdriver.Chrome(driver_path, options=options)
    return webdriver.Chrome(options=options)