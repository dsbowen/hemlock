"""Hemlock debugger"""

from hemlock.debug.run import AIParticipant, run_batch

def debug(num_batches, batch_size):
    [run_batch(int(batch_size)) for i in range(int(num_batches))]