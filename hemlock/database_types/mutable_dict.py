##############################################################################
# Mutable Dictionary
# by Dillon Bowen
# last modified 09/06/2019
##############################################################################

from hemlock.factory import db
from flask_sqlalchemy.model import Model
from sqlalchemy.ext.mutable import Mutable
from inspect import getmro

# Mutable Dictionary database type
class MutableDict(db.PickleType):
    pass

# Model shell
class ModelShell():
    # Shell model: store model id and class (table)
    def __init__(self, model):
        self.id = model.id
        self.model_class = model.__class__
        
    # Unshell: query database to return original model
    def unshell(self):
        return self.model_class.query.get(self.id)

# Mutable Dictionary Wrapper
class MutableDictWrapper(Mutable, dict):
    # Coerce regular dictionary to MutableDictWrapper
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableDictWrapper):
            if isinstance(value, dict):
                return MutableDictWrapper(value)
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
        dict.__setitem__(self, key, self.shell(value))
        self.changed()
        
    # Get item after unshelling models in value
    def __getitem__(self, key):
        return self.unshell(dict.__getitem__(self, key))
    
    # Delete item
    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self.changed()
    
    # Shell value
    # store value as ModelShell if value is a model
    # cascading shelling for dictionaries and iterables
    def shell(self, value):
        if Model in getmro(value.__class__):
            return ModelShell(value)
        if isinstance(value, dict):
            return {key: self.shell(v) for key, v in value.items()}
        if isinstance(value, list):
            return type(value)([self.shell(v) for v in value])
        return value
        
    # Unshell value
    # recover model from ModelShell
    # cascading unshelling for dictionaries and iterables
    def unshell(self, value):
        if isinstance(value, ModelShell):
            return value.unshell()
        if isinstance(value, dict):
            return {key: self.unshell(v) for key, v in value.items()}
        if isinstance(value, list):
            return type(value)([self.unshell(v) for v in value])
        return value
        
MutableDictWrapper.associate_with(MutableDict)