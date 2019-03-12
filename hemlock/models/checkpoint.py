


from hemlock.factory import db

'''
HAS TO DO
return index of end of branch
'''

# contains origin id and table (branch or page)
# contains pointer to checkpoint created by self
class Checkpoint():
    # Initialize a checkpoint from origin
    # origin is a branch or a regular page with next function
    # return self
    def _initialize(self, origin=None):
        self._checkpoint = True
        if origin is None:
            return self
        self._next_function = origin._next_function
        self._next_args = origin._next_args
        self._origin_id = origin.id
        self._origin_table = origin.__class__
        return self
        
    # Get the next branch
    def _get_next(self):
        # get next branch
        if self._next_function is None:
            return
        if self._next_args is None:
            next = self._next_function()
        else:
            next = self._next_function(self._next_args)
            
        # assign embedded data to participants
        [e._assign_participant(self._part_id) for e in next._embedded]
        
        # let the origin of the checkpoint point to the next branch
        table = self._origin_table
        if table is not None:
            table.query.get(self._origin_id)._id_next = next.id
            
        # record length of inserted branch
        self._next_len = len(next._page_queue.all())
        
        return next
      
    # Return the index of the next checkpoint
    def _get_branch_end(self):
        return self._queue_order + self._next_len + 1