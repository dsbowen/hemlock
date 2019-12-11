"""Classes and functions for running debug tool"""

from hemlock.database import Participant, Page
from hemlock.tools import chromedriver

from threading import Thread
from time import sleep
import os
import sys
import unittest
import warnings

class AIParticipant(unittest.TestCase):
    @property
    def current_page(self):
        try:
            page_tag = self.driver.find_element_by_tag_name('page')
        except:
            return None
        page_id = page_tag.get_attribute('id').split('-')[-1]
        return Page.query.get(page_id)

    def setUp(self):
        """Push application context and connect webdriver"""
        from app import app
        warnings.simplefilter('ignore', ResourceWarning)
        self.ctx = app.app_context()
        self.ctx.push()
        self.driver = chromedriver()
        print('url root', os.environ.get('URL_ROOT'))
        self.driver.get(os.environ.get('URL_ROOT'))
        print('connected driver')
        self.part = Participant.query.all()[-1]
        super().setUp()

    def test(self):
        while self.current_page is None or not self.current_page.terminal:
            print('current page is', self.current_page)
            try:
                print(self.current_page.terminal)
            except:
                pass
            self.check_internal_server_error()
            if self.current_page is None:
                print('current page is None')
                sleep(3)
            else:
                submit = self.driver.find_element_by_id('forward-button')
                submit.click()

    def check_internal_server_error(self):
        """Assert that page is not Internal Server Error"""
        try:
            h1 = self.driver.find_element_by_tag_name('h1').text
        except:
            h1 = None
        assert h1 != 'Internal Server Error'

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