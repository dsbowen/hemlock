"""FunctionType database type

Assert function attributes of database models are callable.
"""

from sqlalchemy import PickleType

class FunctionType(PickleType):
    @classmethod
    def coerce(cls, key, object):
        assert callable(object)
        return super().coerce(key, object)