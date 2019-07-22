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

DATA_TYPES = ['letters', 'numeric', 'integer']

class AIParticipantBase():
    P_REFRESH = 0.1
    P_BACK = 0.1
    P_NO_ANSWER = 0.1
    P_CLEAR_TEXT = 0.1
    LOG_LETTER_LEN = (0,3)
    P_WHITESPACE = 0.1
    NUMBER_LEN = (0,10)
    DECIMAL_LEN = (0,10)
    P_NEGATIVE = 0.5

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
        questions = self.driver.find_elements_by_class_name('form-group')
        [self.fill_question(q) for q in questions]
        
    # Fill out question
    def fill_question(self, q):
        self.question = q
        if random() < self.P_NO_ANSWER:
            return
        input = q.find_elements_by_tag_name('input')
        print(input)
        qtype = q.get_attribute('type')
        if qtype == 'text':
            self.fill_text()
        if qtype == 'single choice':
            pass
            
    # Fill out text question
    def fill_text(self):
        if random() < self.P_CLEAR_TEXT:
            self.question.clear()
        getattr(self, choice(DATA_TYPES))()
    
    # Letters
    def letters(self):
        data_type = choice(['letters', 'uppercase', 'lowercase', 'mix'])
        if data_type == 'letters':
            keys = string.ascii_letters
        if data_type == 'uppercase':
            keys = string.ascii_uppercase
        if data_type == 'lowercase':
            keys = string.ascii_lowercase
        if data_type == 'mix':
            keys = string.printable
        if choice([True, False]):
            keys = string.ascii_letters
        self.question.send_keys(self.gen_text(keys))

    # Generate text entry using
    def gen_text(self, keys):
        length = int(10**uniform(*self.LOG_LETTER_LEN))
        keys = [choice(keys) for i in range(length)]
        for i in range(len(keys)):
            if random() < self.P_WHITESPACE:
                keys[i] = ' '
        return ''.join(keys)
    
    # Integer
    def integer(self):
        x = self.gen_number()
        self.question.send_keys(str(int(x)))
    
    # Numeric
    def numeric(self):
        x = self.gen_number()
        x = round(x, choice(range(*self.DECIMAL_LEN)))
        self.question.send_keys(str(x))
        
    # Randomly generate a number
    def gen_number(self):
        x = uniform(0, 10**choice(range(*self.NUMBER_LEN)))
        if random() < self.P_NEGATIVE:
            return -x
        return x
        
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