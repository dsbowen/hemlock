"""Hemlock debugger"""

from hemlock.debug.run import AIParticipant, run_batch

def main(num_batches=1, batch_size=1):
    [run_batch(batch_size) for i in range(num_batches)]