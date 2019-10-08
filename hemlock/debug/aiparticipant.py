"""AI Participant base class"""

from app import app
from hemlock.debug.debug_classes import DebugPage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import random, choice, uniform, shuffle
from time import sleep
import string
import warnings
import sys

DATA_TYPES = ['_letters', '_numeric', '_integer']

app.app_context().push()


class AIParticipantBase():
    P_REFRESH = 0.1
    P_BACK = 0.1
    P_NO_ANSWER = 0.1
    P_CLICK = 0.5
    P_CLEAR_TEXT = 0.1
    LOG_LETTER_LEN = (0,3)
    P_WHITESPACE = 0.1
    NUMBER_LEN = (0,10)
    DECIMAL_LEN = (0,10)
    P_NEGATIVE = 0.5
    MAX_WAIT = 30
    WAIT_INCREMENT = 5

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.driver = webdriver.Chrome()
        
    # Test survey with AI participant
    def test(self):
        print('testing')
        self.driver.get(self.SURVEY_URL)
        h1 = None
        completed = False
        print('testing')
        # while not completed:
        #     self._internal_server_error()
            # DebugPage(self).debug()
            # completed = self._navigate()
                
    # Assert heading is not internal server error
    def _internal_server_error(self):
        try:
            h1 = self.driver.find_element_by_tag_name('h1').text
        except:
            h1 = None
        assert h1 != 'Internal Server Error'
    
    # Default page debug function
    def _default_page_debug(self, page):
        self._random_order(page.questions)
    
    # Default question debug function
    def _default_question_debug(self, question):
        if random() < self.P_NO_ANSWER:
            return
        self._random_order(question.choices)
        if question._text_entry is not None:
            self._fill_text_entry(question)
    
    # Default choice debug function
    def _default_choice_debug(self, choice):
        if random() < self.P_CLICK:
            choice.click()
    
    # Call debug functions of objects in list randomly ordered
    def _random_order(self, objects):
        order = list(range(len(objects)))
        shuffle(order)
        [objects[i].debug() for i in order]
            
    # Fill out text question
    def _fill_text_entry(self, question):
        if random() < self.P_CLEAR_TEXT:
            question.clear()
        getattr(self, choice(DATA_TYPES))(question)
    
    # Letters
    def _letters(self, question):
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
        question.send_keys(self._gen_text(keys))

    # Generate text entry using keys
    def _gen_text(self, keys):
        length = int(10**uniform(*self.LOG_LETTER_LEN))
        keys = [choice(keys) for i in range(length)]
        for i in range(len(keys)):
            if random() < self.P_WHITESPACE:
                keys[i] = ' '
        return ''.join(keys)
    
    # Integer
    def _integer(self, question):
        question.send_keys(str(int(self._gen_number())))
    
    # Numeric
    def _numeric(self, question):
        x = self._gen_number()
        x = round(x, choice(range(*self.DECIMAL_LEN)))
        question.send_keys(str(x))
        
    # Randomly generate a number
    def _gen_number(self):
        x = uniform(0, 10**choice(range(*self.NUMBER_LEN)))
        if random() < self.P_NEGATIVE:
            return -x
        return x
        
    # Navigate in unspecified direction (forward, back, refresh)
    def _navigate(self):
        if random() < self.P_REFRESH:
            self.driver.refresh()
            return False
        if random() < self.P_BACK:
            return self._navigate_direction('back-button')
        return self._navigate_direction('forward-button')
        
    # Navigate in a specified direction
    # return True if it is not possible to go forward
    # indicating survey is completed
    def _navigate_direction(self, direction_button, wait=0):
        try:
            self.driver.find_element_by_id(direction_button).click()
            return False
        except:
            pass
        if direction_button == 'back-button':
            return self._navigate_direction('forward-button')
        if wait >= self.MAX_WAIT:
            return True
        wait += self.WAIT_INCREMENT
        return self._navigate_direction('forward-button', wait)

    def tearDown(self):
        self.driver.close()