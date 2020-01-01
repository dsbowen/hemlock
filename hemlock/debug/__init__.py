"""Hemlock debugger

The debugger sends 'AI participants' through the survey. The AI 
participants attempt to break the survey by clicking random objects and 
entering random responses.

AI participants run in batches of specified sizes. For local debugging, I 
recommend a batch size of 1. For production debugging, you can safely go up 
to 3.
"""

from hemlock.debug.run import AIParticipant, run_batch

def debug(num_batches, batch_size):
    [run_batch(int(batch_size)) for i in range(int(num_batches))]