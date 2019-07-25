##############################################################################
# Test a Hemlock survey
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

from hemlock.debug import main, AIParticipantBase
from unittest import TestCase

NUM_BATCHES = 1
BATCH_SIZE = 1

class AIParticipant(AIParticipantBase, TestCase):
    SURVEY_URL = 'https://test235711.herokuapp.com'

    def custom_debug_example(self, question):
        question.send_keys('hello world')

if __name__ == '__main__':
    main(NUM_BATCHES, BATCH_SIZE)