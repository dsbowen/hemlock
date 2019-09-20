"""Interval function types

This function is executed at a regular interval on the Page.
"""

from hemlock.database.types import Function

from sqlalchemy.types import PickleType


class Interval(Function):
    def __init__(self, func=None, seconds=None, args=[], kwargs={}):
        super().__init__(func, args, kwargs)
        self.seconds = seconds


class IntervalType(PickleType):
    pass


Interval.associate_with(IntervalType)