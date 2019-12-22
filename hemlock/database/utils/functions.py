"""Function models

Compile functions are called before a page compiles its html.
Validate functions are called to validate a participant's response.
Submit functions are called after a page has been successfully submitted.
Navigate functions are called when navigating forward to grow new branches.

Note that compile and submit functions act as wrappers for the normal 
workflow.
"""

from hemlock.app import db
from hemlock.database.branch import Branch
from hemlock.database.page import Page
from hemlock.database.data import Question
from hemlock.database.bases import Base

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_function import FunctionMixin
from sqlalchemy_mutable import MutableListType, MutableDictType
from sqlalchemy_orderingitem import OrderingItem


class FunctionMixin_Page_or_Question(FunctionMixin, Base):
    """Function mixin with page or question as parent"""
    @declared_attr
    def _page_id(self):
        return db.Column(db.Integer, db.ForeignKey('page.id'))

    @declared_attr
    def _question_id(self):
        return db.Column(db.Integer, db.ForeignKey('question.id'))
        
    @property
    def parent(self):
        return self.page or self.question

    @parent.setter
    def parent(self, value):
        if isinstance(value, Page):
            self.page = value
        elif isinstance(value, Question):
            self.question = value
        elif value is None:
            self.page = self.question = None
        else:
            raise ValueError('Parent must be a Page or Question')


class Compile(FunctionMixin_Page_or_Question, db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Validate(FunctionMixin_Page_or_Question, db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Submit(FunctionMixin_Page_or_Question, db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Debug(FunctionMixin_Page_or_Question, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __call__(self, driver):
        """Call function with webdriver argument"""
        if self.parent is None:
            return self.func(driver, *self.args, **self.kwargs)
        return self.func(self.parent, driver, *self.args, **self.kwargs)


class Navigate(FunctionMixin, db.Model):
    """
    A Navigate function can have either a branch or page as its parent. 
    """
    id = db.Column(db.Integer, primary_key=True)
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    @property
    def parent(self):
        return self.branch or self.page

    @parent.setter
    def parent(self, value):
        if isinstance(value, Branch):
            self.branch = value
        elif isinstance(value, Page):
            self.page = value
        elif value is None:
            self.branch = self.page = None
        else:
            raise ValueError('Parent must be a Branch or Page')

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
        