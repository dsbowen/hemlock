##############################################################################
# Main debugging function
# by Dillon Bowen
# last modified 07/18/2019
##############################################################################

import unittest
from threading import Thread

# Tests survey with batches of participants
def main(num_batches=1, batch_size=1):
    [run_batch(batch_size) for i in range(num_batches)]
            
# Run a single batch of participants
def run_batch(batch_size):
    threads = [Thread(target=unittest.main, daemon=True)
        for i in range(batch_size)]
    [t.start() for t in threads]
    [t.join() for t in threads]