##############################################################################
# Base class
# by Dillon Bowen
# last modified 09/06/2019
##############################################################################

from sqlalchemy import inspect
from flask_sqlalchemy.model import Model
from random import shuffle



# Base class for Hemlock models
class Base():
    ##########################################################################
    # Set public model attributes
    ##########################################################################
    
    # Set the object text
    def _set_text(self, text):
        self._text = text
        
    # Set an object's function and arguments
    # inputs:
        # func_name: name of the function (object attribute) as string
        # func: callable or None
        # args_name: name of function arguments as string
        # args: may be None or dict
    def _set_function(self, func_name, func, args_name, args):
        if not (func is None or callable(func)):
            raise ValueError('Function must be callable (or None)')
        if not (args is None or type(args) == dict):
            raise ValueError('Arguments must be dictionary (or None)')
            
        setattr(self, func_name, func)
        setattr(self, args_name, args)
            
    # Call a function
    # inputs:
        # object: main object passed to function
        # function: the called function
        # args: additional keyword arguments (dict)
    def _call_function(self, object=None, function=None, args=None):
        if function is None:
            return
        if object is None and args is None:
            return function()
        if object is None and args is not None:
            return function(**args)
        if object is not None and args is None:
            return function(object)
        return function(object, **args)


    
    ##########################################################################
    # Navigation functions common to branch and page    ##########################################################################
    
    # Indicates whether the object is eligible to grow and insert next branch
    # next function must not be None
    # and the next branch must not already be in the participant's branch stack
    def _eligible_to_insert_next(self):
        return (self._next_function is not None
            and self._next_branch not in self._part._branch_stack)
        
    # Grow and return a new branch
    def _grow_branch(self):
        next_branch = self._call_function(
            function=self._next_function, 
            args=self._next_args)

        if next_branch is None:
            return
        
        next_branch._initialize_head_pointer()
        next_branch._origin_page = next_branch._origin_branch = None
        self._next_branch = next_branch
        return next_branch
        
        
        
    ##########################################################################
    # Assign and remove parents
    # Insert and remove children
    ##########################################################################
    
    # General pattern:
    # assumes parent to child relationship is one to many
    # return if None
    # get keys and other variables
    # modify objects
    
    # Assign a child to a parent
    # remove current parent
    # insert to new parent
    def _assign_parent(self, parent, parent_key, index=None):
        if parent is None:
            return
            
        child_key = self._get_to_self_key(parent_key)
            
        self._remove_parent(parent_key)
        parent._insert_children([self], child_key, index)
        
    # Insert a list of new children
    # push current children who appear after starting index back
    # set index for new children to fill the gap
    def _insert_children(self, new_children, child_key, index=None):
        if not new_children:
            return
    
        parent_key = self._get_to_self_key(child_key)
        order_by_key = self._get_order_by_key(child_key)
        current_children = getattr(self, child_key).all()
        index = len(current_children) if index is None else index

        [c._modify_index(len(new_children), order_by_key)
            for c in current_children[index:]]
        [setattr(c, parent_key, self) for c in new_children]
        [new_children[i]._set_index(index+i, order_by_key)
            for i in range(len(new_children))]
            
    # Remove a child from its parent
    def _remove_parent(self, parent_key):
        parent = getattr(self, parent_key)
        if parent is None:
            return
            
        child_key = self._get_to_self_key(parent_key)
        order = getattr(self, parent._get_order_by_key(child_key))
        
        parent._remove_children(child_key, order, order+1)
        
    # Remove a list of children
    # pull current children who appear after end index forward
    # set index and parent of removed children to None
    def _remove_children(self, child_key, start=0, end=None):
        children = getattr(self, child_key).all()
        if not children:
            return
            
        parent_key = self._get_to_self_key(child_key)
        order_by_key = self._get_order_by_key(child_key)
        end = len(children) if end is None else end
        to_remove = children[start:end]
        
        [c._modify_index(start-end, order_by_key) for c in children[end:]]
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
            
    # Get key mapping object to self given key mapping self to object
    def _get_to_self_key(self, to_object_key):
        relationships = list(inspect(self).mapper.relationships)
        relationship = [r for r in relationships
            if r.key==to_object_key]
        if not relationship:
            return
        return relationship[0].back_populates
            
    # Get the child order_by key (attribute)
    def _get_order_by_key(self, child_key):
        relationships = list(inspect(self).mapper.relationships)
        relationship = [r for r in relationships
            if r.key==child_key]
        if not relationship:
            return
        order_by = relationship[0].order_by
        if order_by:
            return order_by[0].key
            
    # Get the relationship key (attribute) mapping object obj1 to object obj2
    def _relationship_key(self, obj1, obj2):
        relationships = list(inspect(obj1).mapper.relationships)
        relationship = [r for r in relationships
            if r.mapper.class_==obj2.__class__]
        if relationship:
            return relationship[0].key
    
    
    
    ##########################################################################
    # Randomize children
    ##########################################################################
    
    # Randomize order of children
    def _randomize_children(self, child_key):
        children = getattr(self, child_key).all()
        if not children:
            return
            
        order_by_key = self._get_order_by_key(child_key)
        order = list(range(len(children)))
        shuffle(order)
        
        [c._set_index(i, order_by_key) for (c,i) in zip(children, order)]