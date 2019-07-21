##############################################################################
# Success Thread class
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

import sys
from threading import Thread

# Success Thread
# operates as normal Thread with success indicator
class SuccessThread(Thread):
    def run(self):
        self.success = Thread.run(self)