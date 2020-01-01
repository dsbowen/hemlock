"""Function models

`Compile` functions are called before a page compiles its HTML.
`Validate` functions are called to validate a participant's response.
`Submit` functions are called after a page has been successfully submitted.
`Navigate` functions are called when navigating forward to grow new branches.

Note that compile and submit functions act as wrappers for the normal 
workflow.

A `Function`'s `parent` may be a `Branch`, `Page`, or `Question`.
"""

from hemlock.app import db
from hemlock.database.bases import Base
from hemlock.database.branch import Branch
from hemlock.database.page import Page
from hemlock.database.question import Question

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_function import FunctionMixin
from sqlalchemy_mutable import MutableListType, MutableDictType


class Function(FunctionMixin, Base):
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def _branch_id(self):
        return db.Column(db.Integer, db.ForeignKey('branch.id'))

    @declared_attr
    def _page_id(self):
        return db.Column(db.Integer, db.ForeignKey('page.id'))

    @declared_attr
    def _question_id(self):
        return db.Column(db.Integer, db.ForeignKey('question.id'))

    @property
    def parent(self):
        if hasattr(self, 'branch') and self.branch is not None:
            return self.branch
        if hasattr(self, 'page') and self.page is not None:
            return self.page
        if hasattr(self, 'question') and self.question is not None:
            return self.question

    @parent.setter
    def parent(self, parent=None):
        """
        Note: the parent must be set *after* the other attributes are set to None. e.g. 
        
        self.page = self.question = None
        self.branch = parent

        Otherwise, `OrderingItem` will clear the index.
        """
        if isinstance(parent, Branch):
            self.page = self.question = None
            self.branch = parent
        elif isinstance(parent, Page):
            self.branch = self.question = None
            self.page = parent
        elif isinstance(parent, Question):
            self.branch = self.page = None
            self.question = parent
        elif parent is None:
            self.branch = self.page = self.question = None
        else:
            raise ValueError('Parent must be Branch, Page, or Question')

    @Base.init()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Compile(Function, db.Model):
    pass

class Validate(Function, db.Model):
    pass

class Submit(Function, db.Model):
    pass

class Debug(Function, db.Model):
    def __call__(self, driver):
        """Call function with webdriver argument"""
        if self.parent is None:
            return self.func(driver, *self.args, **self.kwargs)
        return self.func(
            self.parent, driver, *self.args, **self.kwargs.unshell()
        )

class Navigate(Function, db.Model):
    def __call__(self):
        """
        A Navigate function call begins by creating a new branch using its 
        function (super().__call__()). It then sets the next_branch and 
        origin relationships between its parent and the new branch. Finally, 
        it sets the head of the new branch's page queue.
        """
        next_branch = super().__call__()
        assert isinstance(next_branch, Branch)
        if self.parent is not None:
            self._set_relationships(self.parent, next_branch)
        next_branch.current_page = next_branch.start_page
        return next_branch

    def _set_relationships(self, parent, next_branch):
        """Set relationships between next_branch and its origin"""
        parent.next_branch = next_branch
        if isinstance(parent, Branch):
            next_branch.origin_branch = parent
            next_branch.origin_page = None
        else:
            next_branch.origin_branch = None
            next_branch.origin_page = parent