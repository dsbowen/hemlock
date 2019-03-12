###############################################################################
# Base class
# by Dillon Bowen
# last modified 03/12/2019
###############################################################################

from hemlock.factory import db
from sqlalchemy import inspect
from random import shuffle

# Base class for Hemlock models
class Base():        
    # Set the object text
    def _set_text(self, text):
        self._text = text
        
    # Set the all_rows indicator
    def _set_all_rows(self, all_rows=True):
        self._all_rows = all_rows
          
    # Get the relationship key mapping object obj1 to object obj2
    def _relationship_key(self, obj1, obj2):
        relationships = list(inspect(obj1).mapper.relationships)
        relationship = [r for r in relationships
            if r.mapper.class_==obj2.__class__]
        if relationship:
            return relationship[0].key
    
    # Get a list of children (siblings) given parent
    def _get_children(self, parent):
        key = self._relationship_key(parent, self)
        return getattr(parent, key).all()
        
    # Assign an object to its parent
    def _assign_parent(self, parent, order=None):
        if parent is None:
            return
          
        # remove from old parent; assign to new parent
        parent_key = self._relationship_key(self, parent)
        self._remove_parent(parent_key)
        setattr(self, parent_key, parent)
        
        # set the order
        children = self._get_children(parent)
        if order is None:
            self._set_order(len(children))
            return
        if order > len(children):
            raise ValueError('Order out of range')
        self._set_order(order)
        children_sorted = sorted(children, key=lambda x: x._order)
        [c._increment_order() for c in children_sorted[order:]]
        
    # Increment order
    def _increment_order(self):
        self._order += 1
        
    # Remove object from its parent given parent key
    def _remove_parent(self, parent_key):
        parent = getattr(self, parent_key)
        if parent is None:
            return
        children = self._get_children(parent)
        children_sorted = sorted(children, key=lambda x: x._order)
        [c._decrement_order() for c in children_sorted[self._order:]]
        setattr(self, parent_key, None)
        
    # Decrement order
    def _decrement_order(self):
        self._order -= 1
        
    # Set order
    def _set_order(self, order):
        self._order = order
        
    '''
    Set an object's function and arguments
    inputs:
        func_name: name of the function (object attribute) as string
        func: callable or None
        args_name: name of function arguments as string
        args: may be None
    '''
    def _set_function(self, func_name, func, args_name, args):
        if func is not None:
            setattr(self, func_name, func)
        if args is not None:
            setattr(self, args_name, args)
            
    '''
    Call a function
    inputs:
        object: main object passed to function
        function: the called function
        args: additional arguments
    '''
    def _call_function(self, object, function, args):
        if function is None:
            return
        if args is None:
            return function(object)
        return function(object, args)
            
    # Randomize order of children
    def _randomize_children(self, children):
        if not children:
            return
        order = list(range(1,len(children)+1))
        shuffle(order)
        [c._set_order(i) for (c,i) in zip(children, order)]