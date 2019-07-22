##############################################################################
# Test a Hemlock survey
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

from hemlock.debug import main, AIParticipantBase
from unittest import TestCase

BATCH_SIZE = 5
NUM_BATCHES = 3

class AIParticipant(AIParticipantBase, TestCase):
    SURVEY_URL = 'https://test235711.herokuapp.com'
    P_NO_ANSWER = 0.6

main(NUM_BATCHES, BATCH_SIZE)