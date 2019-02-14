###############################################################################
# Base class
# by Dillon Bowen
# last modified 02/14/2019
###############################################################################

from hemlock import db
from sqlalchemy import inspect
from random import shuffle

# Base class for Hemlock models
class Base():        
    # Set the object text
    def _set_text(self, text):
        self._text = text
        
    # Set the variable to which the object contributes
    def _set_var(self, var):
        self._var = var
        
    # Set the all_rows indicator
    def _set_all_rows(self, all_rows=True):
        self._all_rows = all_rows
        
    # Set the randomization on/off (True/False)
    def _set_randomize(self, randomize=True):
        self._randomize = randomize
        
    # Set the conditions for clearing the object
    def _set_clear_on(self, clear_on=[]):
        self._clear_on = clear_on
        
    # Assign an object to a participant
    def _assign_participant(self, part):
        self._part = part
        db.session.commit()
        try:
            self._set_vorder()
        except:
            pass
            
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
            
        parent_key = self._relationship_key(self, parent)
    
        # remove current parent
        self._remove_parent(parent_key)
            
        # assign parent
        setattr(self, parent_key, parent)
        
        # get children
        children = self._get_children(parent)

        # set the order
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
        curr_function - name of the current function as string
        new_function - callable or None
        curr_args - name of current arguments as string
        new_args - may be None
    '''
    def _set_function(self, curr_func, new_func, curr_args, new_args):
        if new_func is not None:
            setattr(self, curr_func, new_func)
        if new_args is not None:
            setattr(self, curr_args, new_args)
            
    '''
    Call a function
    inputs:
        object - main object passed to function
        function - the called function
        args - additional arguments
    '''
    def _call_function(self, object, function, args):
        if function is None:
            return
        if args is None:
            return function(object)
        return function(object, args)

    # Get the next branch
    def _get_next(self):
        if self._next_function is not None:
            if self._next_args is None:
                branch = self._next_function()
            else:
                branch = self._next_function(self._next_args)
            [e._assign_participant(self._part) for e in branch._embedded]
            if branch._randomize:
                branch._randomize_children(branch._page_queue.all())
            return branch
        
    # Execute render function and randomization on first render
    def _first_rendition(self, children):
        self._call_function(self, self._render_function, self._render_args)
        if self._randomize:
            self._randomize_children(children)
            
    # Randomize order of children
    def _randomize_children(self, children):
        if not children:
            return
        order = list(range(1,len(children)+1))
        shuffle(order)
        [c._set_order(i) for (c,i) in zip(children, order)]
        
    # Copy data from orig object in self
    # data = columns - foreign keys - id (primary key)
    def _copy(self, orig):
        # copy data
        keys = [c.key for c in orig.__table__.c 
            if c.key!='id' and not c.key.endswith('_id')]
        for k in keys:
            setattr(self, k, getattr(orig, k))
            
        # copy children
        mapper = inspect(orig).mapper
        keys = [r.key for r in mapper.relationships
            if r.direction.name=='ONETOMANY']
            
        k = keys[0]
        orig_children = getattr(orig,k).all()
        if orig_children:
            first = orig_children[0]
            new = first__class__()
            new._assign_parent(self)
        
        # for each child relationship
        #  create children
        #  copy children
        # setattr(self, k, 
            
        return keys
        