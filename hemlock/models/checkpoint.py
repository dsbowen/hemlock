###############################################################################
# Checkpoint sub-class for Page model
# by Dillon Bowen
# last modified 03/15/2019
###############################################################################

from hemlock.factory import db

# contains origin id and table (branch or page)
# contains pointer to checkpoint created by self
class Checkpoint():
    # Initialize a checkpoint from origin
    # origin is a branch or a regular page with next function
    # return self
    def _initialize_as_checkpoint(self, origin=None):
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
        
        # let the origin of the checkpoint point to the next branch
        table = self._origin_table
        if table is not None:
            table.query.get(self._origin_id)._id_next = next.id
            
        # record length of inserted branch
        self._next_len = len(next._page_queue.all())
        
        return next
        
    # Returns the indicies of the start and end of the checkpoint's branch
    # retain checkpoint if originated by Branch (start after self._queue_order)
    # remove checkpoint if originated by Page (start at self._queue_order)
    def _get_branch_endpoints(self):
        from hemlock.models import Branch
        start = self._queue_order
        if self._origin_table == Branch:
            start += 1
            
        end = self._queue_order + self._next_len + 1
        
        return (start, end+1)