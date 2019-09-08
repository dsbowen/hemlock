##############################################################################
# Model Shell
# by Dillon Bowen
# last modified 09/07/2019
##############################################################################

from flask_sqlalchemy.model import Model
from sqlalchemy.ext.mutable import Mutable
from inspect import getmro

# Model shell
class ModelShell():
    # Shell model: store model id and class (table)
    def __init__(self, model):
        self.id = model.id
        self.model_class = model.__class__
        
    # Unshell: query database to return original model
    def unshell(self):
        return self.model_class.query.get(self.id)
        
# Value shell
class ValueShell(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        print('coercing', value)
        if not isinstance(value, ValueShell):
            return ValueShell(value)
        return value

    # Set value and shell
    def __init__(self, value, parent=None):
        print('init')
        print('parent', parent)
        self.value_type = type(value)
        self.value = self.shell(value)
        self.parent = parent
        
    # Get state
    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_parents', None)
        return d
        
    # Set item
    def __setitem__(self, key, value):
        self.value.__setitem__(key, ValueShell(value, self))
        self._changed()
        
    def _changed(self):
        if self.parent is not None:
            print('changing parent')
            self.parent._changed()
        else:
            print('changing self')
            self.changed()
        
    # Get item
    def __getitem__(self, key):
        return self.value.__getitem__(key)
        
    # Delete item
    def __delitem__(self, key):
        self.value_type.__delitem__(self, key)
        self.changed()
        
    # Shell value
    def shell(self, value):
        if Model in getmro(value.__class__):
            return ModelShell(value)
        if isinstance(value, dict):
            print('shelling dict')
            return {key: ValueShell(v, self) for key, v in value.items()}
        if not isinstance(value, str):
            try:
                value_as_list = [ValueShell(v, self) for v in value]
                return type(value)(value_as_list)
            except:
                pass
        return value

    # Unshell value
    def unshell(self):
        if isinstance(self.value, ModelShell):
            return self.value.unshell()
        if isinstance(self.value, dict):
            return {key: val.unshell() for key, val in self.value.items()}
        if not isinstance(self.value, str):
            try:
                value_as_list = [val.unshell() for val in value]
                return self.value_type(value_as_list)
            except:
                pass
        return self.value
        
from hemlock.factory import db
class MutableFlex(db.PickleType):
    pass
    
ValueShell.associate_with(MutableFlex)