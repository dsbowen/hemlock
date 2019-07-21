##############################################################################
# AI Participant Base class
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import random
import warnings

class AIParticipantBase():
    P_REFRESH = 0.1
    P_BACK = 0.1

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
        qtype = q.get_attribute('type')
        if qtype == 'text':
            self.fill_text(q)
            
    # Fill out text question
    def fill_text(self, q):
        q.send_keys('Hello world') ## More on this
        
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