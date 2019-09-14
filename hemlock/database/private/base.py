"""Base classes for public database models

Defines generic Base class and BranchingBase with methods for growing and
inserting new branches to a Participant's branch_stack.
"""

class Base():
    """Generic base class for public database models"""  
    
    def _set_parent(self, parent, index, parent_attr, child_attr):
        """Set model parent
        
        Automatically detect whether to insert using standard __setattr___
        or insert.
        """
        if parent is None or index is None:
            self.__setattr__(parent_attr, parent)
        else:
            getattr(parent, child_attr).insert(index, self)


class BranchingBase(Base):
    """Base class for Branch and Page models
    
    Defines additional methods for growing new branches.
    """
    
    def _eligible_to_insert_next(self):
        """Indicate that object is eligible to grow and insert next branch
        
        A Page or Branch is eligible to insert the next branch to the
        Participant's branch_stack iff the next function is not None and
        the next branch is not already in the branch_stack.
        """
        return (
            self.next is not None
            and self.next_branch not in self.part.branch_stack
            )
        
    def _grow_branch(self):
        """Grow and return a new branch"""
        from hemlock.models import Branch, Page
        
        next_branch = self.next.call(object=self)
        if next_branch is None:
            return
        
        self.next_branch = next_branch
        next_branch.origin_branch = self if isinstance(self, Branch) else None
        next_branch.origin_page = self if isinstance(self, Page) else None
        next_branch._initialize_head_pointer()
        return next_branch