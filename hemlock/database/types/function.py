"""Function type

Tracks a function and its arguments (and keyword arguments).
"""

from sqlalchemy.types import PickleType
from sqlalchemy_mutable import Mutable


class Function(Mutable):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if value is None or callable(value):
            return cls(value)
        raise ValueError(
            'Function attribute must be assigned with callable or Function object'
            )
        
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
        
    def __init__(self, func=None, args=[], kwargs={}):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        
    @property
    def func(self):
        return self._func
    
    @func.setter
    def func(self, value):
        assert value is None or callable(value), (
            'Attempted to set function attribute to non-function value'
            )
        self._func = value
    
    @property
    def args(self):
        return self._args
        
    @args.setter
    def args(self, value):
        assert isinstance(value, list), (
            'Attempted to set arguments attribute to non-list value'
            )
        self._args = value
    
    @property
    def kwargs(self):
        return self._kwargs
        
    @kwargs.setter
    def kwargs(self, value):
        assert isinstance(value, dict), (
            'Attempted to set keyword arguments attribute to non-dict value'
            )
        self._kwargs = value
        
    def __call__(self, object=None):
        if self.func is None:
            return
        if object is None:
            return self.func(*self.args, **self.kwargs)
        return self.func(object, *self.args, **self.kwargs)


class FunctionType(PickleType):
    pass
    
Function.associate_with(FunctionType)