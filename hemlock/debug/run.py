"""Classes and functions for running debug tool"""

from hemlock.database import Participant, Page
from hemlock.tools import chromedriver

from threading import Thread
from time import sleep
import os
import sys
import unittest
import warnings

ERROR_MSG = '{ai.part} encountered an error.'


class AIParticipant(unittest.TestCase):
    def setUp(self):
        """Push application context and connect webdriver"""
        from app import app
        warnings.simplefilter('ignore', ResourceWarning)
        self.ctx = app.app_context()
        self.ctx.push()
        self.driver = chromedriver()
        self.driver.get(os.environ.get('URL_ROOT')+'?Test=1')
        self.part = Participant.query.all()[-1]
        super().setUp()

    def test(self):
        """Take the survey and test for errors"""
        current_page = self.get_current_page()
        while current_page is None or not current_page.terminal:
            self.check_for_error()
            if current_page is None:
                self.driver.refresh()
                sleep(3)
            else:
                current_page._debug(self.driver)
            current_page = self.get_current_page()

    def get_current_page(self):
        """Get the current page"""
        try:
            page_tag = self.driver.find_element_by_tag_name('page')
        except:
            return None
        page_id = page_tag.get_attribute('id').split('-')[-1]
        return Page.query.get(page_id)

    def check_for_error(self):
        """Assert that page is not Internal Server Error"""
        try:
            h1 = self.driver.find_element_by_tag_name('h1').text
        except:
            h1 = ''
        assert h1 != 'Internal Server Error', ERROR_MSG.format(ai=self)

    def tearDown(self):
        """Close webdriver and pop application context"""
        self.driver.close()
        self.ctx.pop()
        super().tearDown()


class SuccessThread(Thread):
    """Operates as normal thread with success indicator"""
    def run(self):
        try:
            Thread.run(self)
            self.success = True
        except:
            self.success = False

def run_batch(batch_size):
    """Run a batch of participants"""
    threads = [
        SuccessThread(target=run_participant, daemon=True)
        for i in range(batch_size)
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
    if not all([t.success for t in threads]):
        sys.exit()

def run_participant():
    """Run a single participant"""
    result = unittest.main(exit=False).result
    assert not result.failures and not result.errors