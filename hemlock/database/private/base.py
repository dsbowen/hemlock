"""Base classes for public database models

Base is a generic base class for all Hemlock models. 

BranchingBase contains methods for growing and inserting new branches to a 
Participant's branch_stack. 

CompileBase contains convenience methods for models which compile html.
"""

from hemlock.app.factory import db

from bs4 import BeautifulSoup
from flask import Markup


class Base():
    @property
    def model_id(self):
        """ID for distinguishing models"""
        return type(self).__name__+'-'+str(self.id)
    
    def __init__(self, *args, **kwargs):
        """Add and flush all models on construction"""
        db.session.add(self)
        db.session.flush([self])
        super().__init__(*args, **kwargs)
    
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
    
    def _eligible_to_insert_branch(self):
        """Indicate that object is eligible to grow and insert next branch
        
        A Page or Branch is eligible to insert the next branch to the
        Participant's branch_stack iff the navigate function is not None and
        the next branch is not already in the branch_stack.
        """
        return (
            self.navigate.func is not None
            and self.next_branch not in self.part.branch_stack
            )
        
    def _grow_branch(self):
        """Grow and return a new branch"""
        from hemlock.database.models import Branch, Page
        
        next_branch = self.navigate(object=self)
        if next_branch is None:
            return
        assert isinstance(next_branch, Branch)
        
        self.next_branch = next_branch
        next_branch.origin_branch = self if isinstance(self, Branch) else None
        next_branch.origin_page = self if isinstance(self, Page) else None
        next_branch.current_page = next_branch.start_page
        return next_branch


class CompileBase(Base):
    def render(self, html=None):
        """Get and prettify compiled html
        
        CompileBase expects Models which inherit it to have a compile_html() method. The compile_html() method returns raw html.
        """
        html = self.compile_html() if html is None else html
        soup = BeautifulSoup(html, 'html.parser')
        return soup.prettify()
    
    def view_html(self, html=None):
        print(self.render(html))