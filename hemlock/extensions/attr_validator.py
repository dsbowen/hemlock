##############################################################################
# Attribute Validator
# by Dillon Bowen
# last modified 09/06/2019
##############################################################################

from hemlock.extensions.extensions_base import ExtensionsBase

# Attribute Validator class
class AttrValidator(ExtensionsBase):
    # Validators is {(model_class, attribute name): validation function}
    def __init__(self):
        self.validators = {}
        
    def init_app(self, app):
        self._register_app(app, ext_name='attr_validator')
    
    # Register validation function
    # arguments:
        # model_class: class of the model to which the attribute belongs
        # attrs: (list of) attribute name(s) to which validation applies
    def register(self, model_class, attrs):
        if isinstance(attrs, str):
            attrs = [attrs]
        if not isinstance(attrs, list):
            raise ValueError('Attributes must be list or string')
            
        def original_function(f):
            for attr in attrs:
                self.validators[(model_class, attr)] = f
            return f
        return original_function
    
    # Validate an attribute assigment
    def validate(self, model_class, name, value):
        if (model_class, name) in self.validators:
            self.validators[(model_class, name)](value)