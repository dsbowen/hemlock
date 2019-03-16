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
    def _call_function(self, object=None, function=None, args=None):
        if function is None:
            return
        if object is None and args is None:
            return function()
        if object is None and args is not None:
            return function(args)
        if object is not None and args is None:
            return function(object)
        return function(object, args)
        
        
        
    ###########################################################################
    # Assign and remove parents
    # Insert and remove children
    ###########################################################################
    
    # Assign a child to a parent
    # remove previous parent
    # insert to new parent
    def _assign_parent(self, parent, parent_key, child_key, index=None):
        if parent is None:
            return
        self._remove_parent(parent_key, child_key)
        parent._insert_children([self], child_key, index)
        
    # Insert a list of new children
    # push current children who appear after starting index back
    # set index for new children to fill the gap
    def _insert_children(self, new_children, child_key, index=None):
        if not new_children:
            return
    
        order_by_key = self._get_order_by_key(child_key)
        current_children = getattr(self, child_key).all()
        if index is None:
            index = len(current_children)
        [c._modify_index(len(new_children), order_by_key)
            for c in current_children[index:]]
        [new_children[i]._set_index(index+i, order_by_key)
            for i in range(len(new_children))]
            
    # Remove a child from its parent
    def _remove_parent(self, parent_key, child_key):
        parent = getattr(self, parent_key)
        if parent is None:
            return
        order = getattr(self, parent._get_order_by_key(child_key))
        parent._remove_children(child_key, order, order+1)
        
    # Remove a list of children
    def _remove_children(self, child_key, start=0, end=None):
        children = getattr(self, child_key).all()
        if not children:
            return
            
        if end is None:
            end = len(children)
            
        order_by_key = self._get_order_by_key(child_key)
        [c._modify_index(start-end, order_by_key) for c in childre[end:]]
        to_remove = children[start:end]
        [setattr(c, parent_key, None) for c in to_remove]
        [setattr(c, order_by_key, None) for c in to_remove]
    
    # Modify the order in which a child appears among its siblings
    def _modify_index(self, amount, order_by_key=None):
        if order_by_key is None:
            return
        setattr(self, order_by_key, getattr(self, order_by_key)+amount)
        
    # Set the order in which a child appears among its siblings
    def _set_index(self, index, order_by_key=None):
        if order_by_key is None:
            return
        setattr(self, order_by_key, index)
        
    # Get the relationship key (attribute) mapping object obj1 to object obj2
    def _relationship_key(self, obj1, obj2):
        relationships = list(inspect(obj1).mapper.relationships)
        relationship = [r for r in relationships
            if r.mapper.class_==obj2.__class__]
        if relationship:
            return relationship[0].key
            
    # Get the child order_by key (attribute)
    def _get_order_by_key(self, child_key):
        relationships = list(inspect(self).mapper.relationships)
        relationship = [r for r in relationships
            if r.mapper.class_.key==child_key]
        if not relationship:
            return
        order_by = relationship[0].order_by
        if order_by:
            return order_by[0].key
    
    
    
    ###########################################################################
    # Randomize children
    ###########################################################################
    
    # Randomize order of children
    def _randomize_children(self, child_key):
        children = getattr(self, child_key).all()
        if not children:
            return
        order_by_key = self._order_by_key(child_key)
        order = list(range(len(children)))
        shuffle(order)
        [c._set_index(i, order_by_key) for (c,i) in zip(children, order)]