##############################################################################
# Base class
# by Dillon Bowen
# last modified 09/07/2019
##############################################################################

from hemlock.factory import attr_settor, db
from sqlalchemy import inspect
from flask_sqlalchemy.model import Model
from random import shuffle



# Base class for Hemlock models
class Base():
    ##########################################################################
    # Set public model attributes
    ##########################################################################
    
    # Set attribute
    # ensure input value is correct type
    def __setattr__(self, name, value):
        value = attr_settor.set(self, name, value)
        db.Model.__setattr__(self, name, value)
        
    # Set parent
    def _set_parent(self, parent, index, parent_attr, child_attr):
        if parent is None or index is None:
            self.__setattr__(parent_attr, parent)
        else:
            getattr(parent, child_attr).insert(index, self)

    # Call function
    # args is a dict of kwargs
    # object is the object on which the function operates (may be None)
    def _call_function(self, function, args, object=None):
        if function is None:
            return
        if object is None:
            return function(**args)
        return function(object, **args)


    
    ##########################################################################
    # Navigation functions common to branch and page    ##########################################################################
    
    # Indicates whether the object is eligible to grow and insert next branch
    # next function must not be None
    # and the next branch must not already be in participant's branch stack
    def _eligible_to_insert_next(self):
        return (
            self.next is not None
            and self.next_branch not in self._part._branch_stack
            )
        
    # Grow and return a new branch
    def _grow_branch(self):
        next_branch = self._call_function(self.next, self.next_args)
        if next_branch is None:
            return
        
        next_branch._initialize_head_pointer()
        next_branch.origin_page = next_branch.origin_branch = None
        self.next_branch = next_branch
        return next_branch
    
# Validation function ensuring function attribute assigned value is callable
def iscallable(value):
    if not (value is None or callable(value)):
        raise ValueError('Function attribute must be callable (or None)')
    return value