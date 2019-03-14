###############################################################################
# Base class
# by Dillon Bowen
# last modified 03/14/2019
###############################################################################

from hemlock.factory import db
from sqlalchemy import inspect
from random import shuffle

# Base class for Hemlock models
class Base():
    ###########################################################################
    # Set public model attributes
    ###########################################################################
    
    # Set the object text
    def _set_text(self, text):
        self._text = text
        
    # Set the all_rows indicator
    def _set_all_rows(self, all_rows=True):
        self._all_rows = all_rows
        
    # Set an object's function and arguments
    # inputs:
        # func_name: name of the function (object attribute) as string
        # func: callable or None
        # args_name: name of function arguments as string
        # args: may be None
    def _set_function(self, func_name, func, args_name, args):
        if func is not None:
            setattr(self, func_name, func)
        if args is not None:
            setattr(self, args_name, args)
            
    # Call a function
    # inputs:
        # object: main object passed to function
        # function: the called function
        # args: additional arguments
    def _call_function(self, object, function, args):
        if function is None:
            return
        if args is None:
            return function(object)
        return function(object, args)
        
        
        
    ###########################################################################
    # Assign and remove parents
    # Insert and remove children
    ###########################################################################
    
    # Assign a child to a parent
    # remove previous parent
    # insert to new parent
    def _assign_parent(self, parent, order=None):
        if parent is None:
            return
        
        parent_key = self._relationship_key(self, parent)
        self._remove_parent(getattr(self, parent_key))
        parent._insert_children([self], order)
    
    # Insert list of children
    # inputs:
        # to_insert: list of children to be inserted
        # start: index at which insertion should start
    # increment order of current children who appear after new children
    # set order for new children
    # set new children's parent to self
    def _insert_children(self, to_insert, start=None):
        if to_insert is None:
            return
            
        children_key = self._relationship_key(self, to_insert[0])
        children = getattr(self, children_key).all()
        order_by_key = self._order_by_key(to_insert[0])
        if start is None:
            start = len(children)
        [c._modify_order(len(to_insert), order_by_key) 
            for c in children[start:]]
        [to_insert[i]._set_order(start+i, order_by_key)
            for i in range(len(to_insert))]
            
        parent_key = self._relationship_key(to_insert[0], self)
        [setattr(x, parent_key, self) for x in to_insert]
            
    # Remove a child from its parent
    def _remove_parent(self, parent):
        if parent is None:
            return
        children_key = self._relationship_key(parent, self)
        order = getattr(self, parent._order_by_key(self))
        parent._remove_children(children_key, order, order+1)
           
    # Remove list of children
    # inputs:
        # children_key: name of children key/attribute (str)
        # start: starting index of removal (int)
        # end: ending index of removal (int)
    # decrement order for children after end of removed children 
    # set order and parent to None for removed children
    def _remove_children(self, children_key, start=0, end=None):
        children = getattr(self, children_key).all()
        if not children:
            return
            
        if end is None:
            end = len(children)

        order_by_key = self._order_by_key(children[0])
        [c._modify_order(start-end, order_by_key) for c in children[end:]]
        
        parent_key = self._relationship_key(children[0], self)
        to_remove = children[start:end]
        [setattr(c, parent_key, None) for c in to_remove]
        [setattr(c, order_by_key, None) for c in to_remove]
        
    
    # Modify the order in which a child appears among its siblings
    def _modify_order(self, amount, order_by_key=None):
        if order_by_key is None:
            return
        setattr(self, order_by_key, getattr(self, order_by_key)+amount)
        
    # Set the order in which a child appears among its siblings
    def _set_order(self, order, order_by_key=None):
        if order_by_key is None:
            return
        setattr(self, order_by_key, order)
        
    # Get the relationship key (attribute) mapping object obj1 to object obj2
    def _relationship_key(self, obj1, obj2):
        relationships = list(inspect(obj1).mapper.relationships)
        relationship = [r for r in relationships
            if r.mapper.class_==obj2.__class__]
        if relationship:
            return relationship[0].key
            
    # Get the child order_by key (attribute)
    def _order_by_key(self, child):
        relationships = list(inspect(self).mapper.relationships)
        relationship = [r for r in relationships
            if r.mapper.class_==child.__class__]
        if not relationship:
            return
        order_by = relationship[0].order_by
        if order_by:
            return order_by[0].key
    
    
    
    ###########################################################################
    # Randomize children
    ###########################################################################
    
    # Randomize order of children
    def _randomize_children(self, children):
        if not children:
            return
        order_by_key = self._order_by_key(children[0])
        order = list(range(len(children)))
        shuffle(order)
        [c._set_order(i, order_by_key) for (c,i) in zip(children, order)]