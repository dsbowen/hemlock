##############################################################################
# Debug function
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

import unittest
from hemlock.debug.aiparticipant import AIParticipant
from sys import argv

def debug():
    AIParticipant.SURVEY_URL = argv.pop()
    unittest.main()