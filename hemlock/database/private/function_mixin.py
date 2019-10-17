"""Mixin for Function models

A Function model has a parent, a function, args, and kwargs. When called, 
the Function model executes its function, passing in its parent (if 
applicable) and its args and kwargs.
"""

from hemlock.app import db

from sqlalchemy_mutable import MutableListType, MutableDictType


class FunctionMixin():
    id = db.Column(db.Integer, primary_key=True)
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

    def __init__(self, parent=None, func=None, args=[], kwargs={}):
        self.parent = parent
        self.func = func
        self.args, self.kwargs = args, kwargs
        super().__init__()
    
    def __call__(self):
        if self.func is None:
            return
        if not hasattr(self, 'parent'):
            return self.func(*self.args, **self.kwargs)
        return self.func(self.parent, *self.args, **self.kwargs)