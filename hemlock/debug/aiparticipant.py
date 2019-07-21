##############################################################################
# AI Participant Base class
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import random, choice, uniform
import string
import warnings
import sys

# DATA_TYPES = ['letters', 'uppercase', 'lowercase', 'integer', 'numeric', 'all']
DATA_TYPES = ['letters']

class AIParticipantBase():
    P_REFRESH = 0.1
    P_BACK = 0.1
    P_NO_ANSWER = 0.1
    P_CLEAR_TEXT = 0.1
    LOG_LETTER_LEN = (0,3)
    P_WHITESPACE = 0.1
    LOG_NUMBER_LEN = (0,10)

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.driver = webdriver.Chrome()
        
    # Test survey with AI participant
    def test(self):
        self.driver.get(self.SURVEY_URL)
        h1 = None
        completed = False
        while not completed:
            self.internal_server_error()
            self.fill_form()
            completed = self.navigate()
                
    # Assert heading is not internal server error
    def internal_server_error(self):
        try:
            h1 = self.driver.find_element_by_tag_name('h1').text
        except:
            h1 = None
        assert h1 != 'Internal Server Error'
        
    # Fill out form
    def fill_form(self):
        questions = self.driver.find_elements_by_tag_name('input')
        [self.fill_question(q) for q in questions]
        
    # Fill out question
    def fill_question(self, q):
        self.question = q
        if random() < self.P_NO_ANSWER:
            return
        qtype = q.get_attribute('type')
        if qtype == 'text':
            self.fill_text()
            
    # Fill out text question
    def fill_text(self):
        if random() < self.P_CLEAR_TEXT:
            self.question.clear()
        getattr(self, choice(DATA_TYPES))()
    
    # Letters
    def letters(self):
        keys = string.ascii_letters
        key_len = int(10**uniform(*self.LOG_LETTER_LEN))
        keys = [choice(string.ascii_letters) for i in range(key_len)]
        keys = self.whitespace(keys)
        self.question.send_keys(keys)
    
    # Randomly insert white space
    def whitespace(self, keys):
        for i in range(len(keys)):
            if random() < self.P_WHITESPACE:
                keys[i] = ' '
        return ''.join(keys)
        
    # Navigate in unspecified direction (forward, back, refresh)
    def navigate(self):
        if random() < self.P_REFRESH:
            self.driver.refresh()
            return False
        if random() < self.P_BACK:
            return self.navigate_direction('back-button')
        return self.navigate_direction('forward-button')
        
    # Navigate in a specified direction
    # return True if it is not possible to go forward
    # indicating survey is completed
    def navigate_direction(self, direction_button):
        try:
            self.driver.find_element_by_id(direction_button).click()
            return False
        except:
            pass
        if direction_button == 'forward-button':
            return True
        return self.navigate_direction('forward-button')

    def tearDown(self):
        self.driver.close()