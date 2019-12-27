"""Selenium webdrivers"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def chromedriver():
    options = Options()
    # options._arguments = ['--disable-gpu', '--no-sandbox', '--headless']
    options._arguments = ['--disable-gpu', '--no-sandbox']
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    driver_path = os.environ.get('CHROMEDRIVER_PATH')
    if driver_path:
        return webdriver.Chrome(driver_path, options=options)
    return webdriver.Chrome(options=options)