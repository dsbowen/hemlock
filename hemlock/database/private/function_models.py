"""Function Mixin"""

from hemlock.app import db
from hemlock.database.private.base import Base

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_mutable import MutableListType, MutableDictType


class FunctionMixin():
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

    index = db.Column(db.Integer)

    _func = db.Column(db.PickleType)
    args = db.Column(MutableListType)
    kwargs = db.Column(MutableDictType)

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, value):
        assert value is None or callable(value), (
            'Attempted to set function attribute to non-function value'
            )
        self._func = value
    
    @classmethod
    def _parent_attr(cls, parent):
        from hemlock.database.models import Branch, Page, Question
        if isinstance(parent, Branch):
            return 'branch'
        if isinstance(parent, Page):
            return 'page'
        if isinstance(parent, Question):
            return 'question'
        raise ValueError('Parent not recognized')

    def __init__(self, parent=None, func=None, args=[], kwargs={}):
        if parent is not None:
            setattr(self, self._parent_attr(parent), parent)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        super().__init__()
    
    def __call__(self, parent=None):
        if self.func is None:
            return
        if parent is not None:
            pass
        elif hasattr(self, 'branch') and self.branch is not None:
            parent = self.branch
        elif hasattr(self, 'page') and self.page is not None:
            parent = self.page
        elif hasattr(self, 'question') and self.question is not None:
            parent = self.question
        return self.func(parent, *self.args, **self.kwargs)


class CompileFunction(FunctionMixin, Base, db.Model):
    pass

class Validator(FunctionMixin, Base, db.Model):
    pass

class SubmitFunction(FunctionMixin, Base, db.Model):
    pass

class Navigator(FunctionMixin, Base, db.Model):
    pass