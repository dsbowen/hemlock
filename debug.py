##############################################################################
# Test a Hemlock survey
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

from hemlock.debug import main, AIParticipantBase
from unittest import TestCase

BATCH_SIZE = 2
NUM_BATCHES = 3

class AIParticipant(AIParticipantBase, TestCase):
    SURVEY_URL = 'https://test235711.herokuapp.com'
    P_CLEAR_TEXT = 1
    LOG_LETTER_LEN = (0,1)

main(NUM_BATCHES, BATCH_SIZE)