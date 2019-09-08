##############################################################################
# Mutable Dictionary
# by Dillon Bowen
# last modified 09/07/2019
##############################################################################

from hemlock.factory import db
from hemlock.database_types.model_shell import ModelShell
from sqlalchemy.ext.mutable import Mutable

from flask_sqlalchemy.model import Model
from inspect import getmro

# Mutable Dictionary database type
class MutableDict(db.PickleType):
    pass

# Mutable Dictionary Wrapper
class MutableDictWrapper(Mutable, dict):
    # Coerce regular dictionary to MutableDictWrapper
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableDictWrapper):
            if isinstance(value, dict):
                return MutableDictWrapper(value) # shell
            return Mutable.coerce(key, value)
        return value
        
    # Set state
    def __setstate__(self, state):
        self.update(state)
        
    # Get state
    def __getstate__(self):
        return dict(self)
        
    # Set item after shelling models in value
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value) # shell
        self.changed()
        
    # Get item after unshelling models in value
    # def __getitem__(self, key):
        # return dict.__getitem__(unshell(dict(self)), key)
        # print('get item')
        # return dict.__getitem__(dict(self), key)
    
    # Delete item
    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self.changed()
        
# Wrap Mutable Dictionary
MutableDictWrapper.associate_with(MutableDict)