
from hemlock.factory import db
from sqlalchemy.ext.mutable import Mutable

class DictWrapper():
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        
    def __setitem__(self, key, value):
        value = DictWrapper(value, self) if isinstance(value, dict) else value
        self.value[key] = value
        self.changed()
    
    def __getitem__(self, key):
        return self.value[key]
        
    def changed(self):
        self.parent.changed()

class MutableDict(Mutable, DictWrapper):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, MutableDict):
            return value
        if not isinstance(value, dict):
            raise ValueError('MutableDict coerce requires type dict')
        return MutableDict(value)
        
    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_parents', None)
        return d
        
    def changed(self):
        Mutable.changed(self)

class PickleEncodedDict(db.PickleType):
    pass

MutableDict.associate_with(PickleEncodedDict)