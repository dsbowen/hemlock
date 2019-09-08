

from sqlalchemy.ext.mutable import Mutable

class MutableWrapper():
    def __init__(self, value, parent=None):
        self.value, self.parent = self.wrap(value), parent
        
    def __contains__(self, value):
        return self.value.__contains__(value)
        
    def __delattr__(self, name):
        self.value.__delattr__(name)
        self.changed()
        
    def __delitem__(self, key):
        self.value.__delitem__(key)
        self.changed()
    
    def __eq__(self, value):
        return self.value.__eq__(value)
    
    def __ge__(self, value):
        return self.value.__ge__(value)
        
    def __getattribute__(self, name):
        return self.value.__getattribute__(name)
        
    def __getattr__(self, name):
        return self.value.__getattr__(name)
        
    def __getitem__(self, key):
        return self.value.__getitem__(key)
        
    def __gt__(self, value):
        return self.value.__gt__(value)
    
    def __iter__(self):
        return self.value.__iter__()
    
    def __le__(self, value):
        return self.value.__le__(value)
    
    def __len__(self):
        return self.value.__len__()
        
    def __lt__(self, value):
        return self.value.__lt__(value)
        
    def __ne__(self, value):
        return self.value.__ne__(value)
        
    def __repr__(self):
        return self.value.__repr__()
    
    def __setattr__(self, name, value):
        self.value.__setattr__(name, self.wrap(value))
        self.changed()
        
    def __setitem__(self, key, value):
        self.value.__setitem__(name, self.wrap(value))
        self.changed()
        
    def __str__(self):
        return self.value.__str__()
    
    # specific to dictionary
    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_parents', None)
        return d
        
    def changed(self):
        if self.parent is not None:
            self.parent.changed()
        else:
            self.changed()
    
    # Wrap 
    def wrap(self, value):
        self._wrapattrs(value)
        
    # Wrap an object's mutable attributes
    def _wrapattrs(self, value):
        if not hasattr(value, mutable_attrs):
            return value
        for name in value.mutable_attrs:
            try:
                value.__setattr__(name, self.wrap(value.__getattr__(name)))
            except:
                pass
        return value
    