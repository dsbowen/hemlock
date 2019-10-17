"""Function models

Compile functions are called before a page compiles its html.
Validate functions are called to validate a participant's response.
Submit functions are called after a page has been successfully submitted.
Navigate functions are called when navigating forward to grow new branches.

Note that compile and submit functions act as wrappers for the normal 
workflow.
"""

from hemlock.app import db
from hemlock.database import Branch, Page, Question
from hemlock.database.private import Base, FunctionMixin

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_mutable import MutableListType, MutableDictType


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
        return self.page if self.page is not None else self.question

    @parent.setter
    def parent(self, value):
        if isinstance(value, Page):
            self.page = value
            self.question = None
        elif isinstance(value, Question):
            self.page = None
            self.question = value
        elif value is None:
            self.page = self.question = None
        else:
            raise ValueError('Parent must be a Page or Question')


class Compile(FunctionMixin_Page_or_Question, db.Model):
    pass


class Validate(FunctionMixin_Page_or_Question, db.Model):
    pass


class Submit(FunctionMixin_Page_or_Question, db.Model):
    pass


class Navigate(FunctionMixin, Base, db.Model):
    """
    A Navigate function can have either a branch or page as its parent. 
    """
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    @property
    def parent(self):
        return self.branch if self.branch is not None else self.page

    @parent.setter
    def parent(self, value):
        if isinstance(value, Branch):
            self.branch = value
            self.page = None
        elif isinstance(value, Page):
            self.branch = None
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
        