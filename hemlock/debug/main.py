##############################################################################
# Main debugging function
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

import unittest
import sys
from hemlock.debug.success_thread import SuccessThread
from threading import Thread

# Tests survey with batches of participants
def main(num_batches=1, batch_size=1):
    [run_batch(batch_size) for i in range(num_batches)]
            
# Run a batch of participants
def run_batch(batch_size):
    threads = [SuccessThread(target=run_participant, daemon=True)
        for i in range(batch_size)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    if not all([t.success for t in threads]):
        sys.exit(INSIRATIONAL_ERROR_MESSAGE)

# Runs a single participant
def run_participant():
    assert not unittest.main().result.failures
        
INSIRATIONAL_ERROR_MESSAGE = '''
Congratulations!

Your debugging test uncovered an error.

I know this may not sound like good news, but it's better to discover errors now, before you run the actual study. Trust me, I've made some pretty dumb mistakes which ended up costing thousands of research dollars. Not a great feeling.

When you think about it like that, it's actually pretty great news that you found this error. 

And it's all thanks to you being clever enough to run the debugger. Say, I guess that makes you pretty awesome, doesn't it?

So, don't despair! You're amazing! You can do it! Now go fix that damn bug!
'''