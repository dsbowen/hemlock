"""Base classes for public database models

Defines generic Base class and BranchingBase with methods for growing and
inserting new branches to a Participant's branch_stack.
"""

from hemlock.app.factory import db

from bs4 import BeautifulSoup


class Base():
    """Generic base class for public database models"""
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        assert type in self.html_compiler, (
            'Type does not have an associated html compiler'
            )
        self._type = type
        
    @classmethod
    def register(cls, type, registration):
        assert registration in cls.REGISTRATIONS
        def register(func):
            getattr(cls, registration)[type] = func
            return func
        return register
    
    def __init__(self):
        db.session.add(self)
        db.session.flush([self])
    
    def _set_parent(self, parent, index, parent_attr, child_attr):
        """Set model parent
        
        Automatically detect whether to insert using standard __setattr___
        or insert.
        """
        if parent is None or index is None:
            self.__setattr__(parent_attr, parent)
        else:
            getattr(parent, child_attr).insert(index, self)
    
    def _compile_html(self):
        return self.html_compiler[self.type](self)
    
    def view_html(self):
        """View compiled html for debugging purposes"""
        soup = BeautifulSoup(self._compile_html(), 'html.parser')
        print(soup.prettify())
    
    def _get_url(self):
        if self.url is None:
            return '#'
        if self.url.startswith('http'):
            return self.url
        return url_for(self.url)


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