##############################################################################
# Test a Hemlock survey
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

# TODO
# enter data into form fields

from hemlock.debug import main, AIParticipantBase
from unittest import TestCase

BATCH_SIZE = 1
NUM_BATCHES = 1

class AIParticipant(AIParticipantBase, TestCase):
    SURVEY_URL = 'localhost:5000'

main(NUM_BATCHES, BATCH_SIZE)