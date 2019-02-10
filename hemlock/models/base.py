###############################################################################
# Base class
# by Dillon Bowen
# last modified 02/10/2019
###############################################################################

from hemlock import db

# Get the next branch of the survey
# inputs: next navigation function, arguments, participant
# returns branch from the next navigation function
# assigns participant for embedded data questions
class Base():
    # assigns the instance to a participant
    def assign_participant(self, part):
        self.part = part
        db.session.commit()
        
    # assigns an object to its parent
    # inputs:
    #   parent_name - string
    #   parent - object
    #   children - list of children
    #   order - order in which this child appears in children list, int
    # removes child from previous parent (if any)
    # assigs child to new parent
    # determines the order in which the child appears in parent's children
    def assign_parent(self, parent_name, parent, children, order):
        self.remove_parent(parent_name, children)
        setattr(self, parent_name, parent)

        # sets the order
        if order is None:
            self.order = len(children)
            return
        if order > len(children):
            raise ValueError('Order out of range')
        self.order = order
        children_sorted = sorted(children, key=lambda x: x.order)
        [c.increment_order() for c in children_sorted[order:]]
        
    def increment_order(self):
        self.order += 1
        
    # removes an object from its parent
    # inputs:
    #   parent_name - string
    #   children - list of children belonging to parent
    def remove_parent(self, parent_name, children):
        if getattr(self, parent_name) is None:
            return
        setattr(self, parent_name, None)
        children_sorted = sorted(children, key=lambda x: x.order)
        [c.decrement_order() for c in children_sorted[self.order:]]
        self.order = None
        
    def decrement_order(self):
        self.order -= 1
        
    # Sets the next navigation function and arguments
    def set_next(self, next=None, args=None):
        self.set_function('next', next, 'next_args', args)
        
    def set_render(self, render=None, args=None):
        self.set_function('render_function', render, 'render_args', args)
        
    def set_post(self, post=None, args=None):
        self.set_function('post_function', post, 'post_args', args)
        
    # sets a function and arguments
    # inputs:
    #   curr_function - name of the current function as string
    #   new_function - callable or None
    #   curr_args - name of current arguments as string
    #   new_args - may be None
    def set_function(self, curr_func, new_func, curr_args, new_args):
        if new_func is not None:
            setattr(self, curr_func, new_func)
        if new_args is not None:
            setattr(self, curr_args, new_args)
            
    def call_function(self, object, function, args):
        if function is None:
            return
        if args is None:
            return function(object)
        return function(object, args)

    # sets the text for questions and choices
    def set_text(self, text=''):
        self.text = text
        
    # turns randomization on/off for branches, pages, and questions
    def set_randomize(self, randomize=True):
        self.randomize = randomize
        
    # sets the variable in which the data will be stored
    def set_var(self, var):
        self.var = var
        
    # set the all_rows indicator
    # i.e. the data will appear in all of the participant's dataframe rows
    def set_all_rows(self, all_rows=True):
        self.all_rows = all_rows

    # gets the next branch
    # returns None if no next branch
    def get_next(self):
        if self.next:
            if self.next_args is None:
                branch = self.next()
            else:
                branch = self.next(self.next_args)
            for e in branch.embedded:
                e.part = part
            return branch