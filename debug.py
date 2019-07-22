##############################################################################
# Test a Hemlock survey
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

from hemlock.debug import main, AIParticipantBase
from unittest import TestCase

BATCH_SIZE = 1
NUM_BATCHES = 1

class AIParticipant(AIParticipantBase, TestCase):
    SURVEY_URL = 'https://test235711.herokuapp.com'

main(NUM_BATCHES, BATCH_SIZE)