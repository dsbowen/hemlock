##############################################################################
# Attribute Settor
# by Dillon Bowen
# last modified 09/06/2019
##############################################################################

from hemlock.extensions.extensions_base import ExtensionsBase

# Attribute Settor class
class AttrSettor(ExtensionsBase):
    # set_functions is {(model_class, attribute name): set function}
    def __init__(self):
        self.set_functions = {}
        
    def init_app(self, app):
        self._register_app(app, ext_name='attr_validator')
    
    # Register set function
    # arguments:
        # model_class: class of the model to which the attribute belongs
        # attrs: (list of) attribute name(s) to which set function applies
    def register(self, model_class, attrs):
        if isinstance(attrs, str):
            attrs = [attrs]
        if not isinstance(attrs, list):
            raise ValueError('Attributes must be list or string')
            
        def original_function(f):
            for attr in attrs:
                self.set_functions[(model_class, attr)] = f
            return f
        return original_function
    
    # Set the value of an attribute assigment
    def set(self, model, name, value):
        if (model.__class__, name) in self.set_functions:
            return self.set_functions[(model.__class__, name)](model, value)
        return value