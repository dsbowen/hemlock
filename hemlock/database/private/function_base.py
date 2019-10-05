"""Base classes for models which use Function models"""

from hemlock.database.private.base import Base
from hemlock.database.private.function_models import FunctionMixin, GetFunction, Validator, PostFunction, Navigator


class FunctionBase(Base):
    """Base for classes with relationships to Function models"""
    @property
    def get_functions(self):
        return self._get_functions
    
    @get_functions.setter
    def get_functions(self, get_functions):
        self._get_functions = self._to_function_models(
            get_functions, GetFunction
        )
    
    @property
    def validators(self):
        return self._validators
    
    @validators.setter
    def validators(self, validators):
        self._validators = self._to_function_models(validators, Validator)
    
    @property
    def post_functions(self):
        return self._post_functions
    
    @post_functions.setter
    def post_functions(self, post_functions):
        self._post_functions = self._to_function_models(
            post_functions, PostFunction
        )
    
    @property
    def navigator(self):
        return self._navigator

    @navigator.setter
    def navigator(self, navigator):
        self._navigator = self._to_function_model(navigator, Navigator)

    def _to_function_model(self, func, model):
        """Convert a function to a Function model"""
        if func is None:
            return
        return func if isinstance(func, FunctionMixin) else model(self, func)
    
    def _to_function_models(self, funcs, model):
        """Convert a list of functions to Function models"""
        funcs = funcs if isinstance(funcs, list) else [funcs]
        return [self._to_function_model(f, model) for f in funcs]


class BranchingBase(FunctionBase):
    """Base class for Branch and Page models
    
    Defines additional methods for growing new branches.
    """
    
    def _eligible_to_insert_branch(self):
        """Indicate that object is eligible to grow and insert next branch
        
        A Page or Branch is eligible to insert the next branch to the
        Participant's branch_stack iff the navigator is not None and
        the next branch is not already in the branch_stack.
        """
        return (
            self.navigator and self.next_branch not in self.part.branch_stack
        )
        
    def _grow_branch(self):
        """Grow and return a new branch"""
        from hemlock.database.models import Branch, Page
        
        next_branch = self.navigator()
        if next_branch is None:
            return
        assert isinstance(next_branch, Branch)
        
        self.next_branch = next_branch
        next_branch.origin_branch = self if isinstance(self, Branch) else None
        next_branch.origin_page = self if isinstance(self, Page) else None
        next_branch.current_page = next_branch.start_page
        return next_branch