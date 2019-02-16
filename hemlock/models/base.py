###############################################################################
# Base class
# by Dillon Bowen
# last modified 02/14/2019
###############################################################################

from hemlock import db
from sqlalchemy import inspect
from random import shuffle

# Intersection of two lists by attr key
# return list of [l1 elements, l2 elements]
# key must be unique in each list
def intersection_by_key(l1, l2, key):
    key1, key2 = [[getattr(item,key) for item in l] for l in [l1,l2]]
    common_keys = set(key1) & set(key2)
    return [[item 
        for item in l if getattr(item,key) in common_keys]
        for l in [l1,l2]]

# Base class for Hemlock models
class Base():        
    # Add the object to database and commit
    def _add_commit(self):
        db.session.add(self)
        db.session.commit()
        try:
            self._id_orig = self.id
        except:
            pass

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
            # [e._assign_participant(self._part) for e in branch._embedded]
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
    def _copy(self, orig_id):
        orig = self.__class__.query.get(orig_id)
    
        # copy data
        keys = [c.key for c in orig.__table__.c 
            if c.key!='id' and not c.key.endswith('_id')]
        for k in keys:
            setattr(self, k, getattr(orig, k))
            
        # copy children
        mapper = inspect(orig).mapper
        keys = [r.key for r in mapper.relationships
            if r.direction.name=='ONETOMANY']
           
        for key in keys: 
            # get all children
            orig_children = getattr(orig, key).all()
            self_children = getattr(self, key).all()
            
            # common children
            self_common, orig_common = intersection_by_key(
                self_children, orig_children,'_id_orig')
            for i in range(len(self_common)):
                self_common[i]._copy(orig_common[i].id)
                
            # children unique to self
            for child in [c for c in self_children if c not in self_common]:
                parent_key = self._relationship_key(child, self)
                child._remove_parent(parent_key)
                
            # children unique to orig
            for child in [c for c in orig_children if c not in orig_common]:
                new_child = child.__class__()
                new_child._assign_parent(self)
                new_child._copy(child.id)
        