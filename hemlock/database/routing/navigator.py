
from hemlock.app import db

from sqlalchemy_mutable import MutableType

def set_forward_route(func):
    """Set the forward route as the function name"""
    def with_route_setting(part):
        part._forward_route = func.__name__
        return func()
    return with_route_setting


@set_forward_route
class ForwardFunctionsMixin():
    _origin = db.Column(MutableType)

    """Forward navigation"""
    def _forward(self):
        """Advance forward to specified Page"""
        if self._forward_to_id is None:
            return self._forward_one()
        while self.current_page.id != self._forward_to_id:
            loading_page = self._forward_one()
            if loading_page is not None:
                return loading_page
    
    def _forward_one(self):
        """Advance forward one page"""
        page = self.current_page
        if page._eligible_to_insert_branch():
            return self._insert_branch(page)
        else:
            self.current_branch._forward()
        return self._forward_recurse()
    
    def _insert_branch(self, origin=None):
        """Grow and insert new branch into the branch stack"""
        origin = origin or self._origin
        self._origin = origin
        loading_page = self._handle_worker(
            origin.navigate, origin.navigate_worker
        )
        if loading_page is not None:
            return loading_page
        branch = origin.next_branch
        self.branch_stack.insert(self.current_branch.index+1, branch)
        self._increment_head()
        return self._forward_recurse()
        
    def _forward_recurse(self):
        """Recursive forward function
        
        Advance forward until the next Page is found (i.e. is not None).
        """
        if self.current_page is not None:
            return
        branch = self.current_branch
        if branch._eligible_to_insert_branch():
            return self._insert_branch(branch)
        else:
            self._decrement_head()
            branch._forward()
        return self._forward_recurse()
    
    """Backward navigation"""
    def _back(self):
        """Navigate backward to specified Page"""
        back_to = self.current_page.back_to
        if back_to is None:
            return self._back_one()
        while self.current_page.id != back_to.id:
            self._back_one()
            
    def _back_one(self):
        """Navigate backward one Page"""      
        if self.current_page == self.current_branch.start_page:
            self._remove_branch()
        else:
            self.current_branch._back()
        self._back_recurse()
        
    def _remove_branch(self):
        """Remove current branch from the branch stack"""
        self._decrement_head()
        self.branch_stack.pop(self.current_branch.index+1)
        
    def _back_recurse(self):
        """Recursive back function
        
        Navigate backward until previous Page is found.
        """
        if self._found_previous_page():
            return
        if self.current_page is None:
            if self.current_branch.next_branch in self.branch_stack:
                self._increment_head()
            elif not self.current_branch.pages:
                self._remove_branch()
            else:
                self.current_branch._back()
        else:
            self._increment_head()
        self._back_recurse()
    
    def _found_previous_page(self):
        """Indicate that previous page has been found in backward navigation
        
        The previous page has been found when 1) the Page is not None and
        2) it does not branch off to another Branch in the stack.
        """
        return (
            self.current_page is not None 
            and self.current_page.next_branch not in self.branch_stack
        )

    """General navigation and debugging"""
    def _increment_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index+1]
    
    def _decrement_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index-1]
    
    def _view_nav(self):
        """Print branch stack for debugging purposes"""
        self.branch_stack[0].view_nav()