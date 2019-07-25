##############################################################################
# Test a Hemlock survey
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

from hemlock.debug import main, AIParticipantBase
from unittest import TestCase

NUM_BATCHES = 1
BATCH_SIZE = 1

class AIParticipant(AIParticipantBase, TestCase):
    SURVEY_URL = 'https://test235711.herokuapp.com'
    P_CLEAR_TEXT = 1
    LOG_LETTER_LEN = (0,1)
    
    def debug_test(self, page):
        [q.send_keys(page.test) for q in page.questions]
    
    def debug_test2(self, question, hello):
        question.send_keys('hello '+hello)
    
    def debug_test3(self, choice):
        choice.click()

if __name__ == '__main__':
    main(NUM_BATCHES, BATCH_SIZE)