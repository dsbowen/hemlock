"""Base classes for public database models

Base is a generic base class for all Hemlock models. 

BranchingBase contains methods for growing and inserting new branches to a 
Participant's branch_stack. 

CompileBase contains convenience methods for models which compile html.

FunctionBase contains convenience methods for models with relationships to 
Function models.
"""

from hemlock.app import db
from hemlock.database.private.function_mixin import FunctionMixin

from bs4 import BeautifulSoup
from sqlalchemy.inspection import inspect


class Base():
    @property
    def model_id(self):
        """ID for distinguishing models"""
        id = inspect(self).identity
        id = '-'.join([str(key) for key in id]) if id is not None else ''
        return type(self).__name__+'-'+str(id)
    
    def __init__(self, settings={}, *args, **kwargs):
        """Add and flush all models on construction"""
        for name, value in settings.items():
            if not hasattr(self, name) or not getattr(self, name):
                setattr(self, name, value)
        super().__init__(*args, **kwargs)
        db.session.add(self)
        db.session.flush([self])
    
    def _set_parent(self, parent, index, parent_attr, child_attr):
        """Set model parent
        
        Automatically detect whether to insert using standard __setattr___
        or insert.
        """
        if parent is None or index is None:
            self.__setattr__(parent_attr, parent)
        else:
            getattr(parent, child_attr).insert(index, self)


class BranchingBase(Base):
    def _eligible_to_insert_branch(self):
        """Indicate that object is eligible to grow and insert next branch
        
        A Page or Branch is eligible to insert the next branch to the
        Participant's branch_stack iff the navigator is not None and
        the next branch is not already in the branch_stack.
        """
        return (
            self.navigate_function is not None 
            and self.next_branch not in self.part.branch_stack
        )


class CompileBase(Base):
    def _render(self, html=None):
        """Get and prettify compiled html
        
        CompileBase expects Models which inherit it to have a _compile method.
        """
        html = self._compile() if html is None else html
        return BeautifulSoup(html, 'html.parser').prettify()
    
    def view_html(self, html=None):
        print(self.render(html))


class FunctionBase(Base):
    """Function base mixin

    Models with relationships to Function models should inherit this base. 
    They should call _set_function_relationships before any function 
    attributes are set.
    
    Users can then set function attributes to functions instead of Function 
    models. When set to functions, FunctionBase will automatically convert the
    functions to Function models.

    e.g. the following commands are equivalent:
    model.function = function 
    model.function = Function(parent=model, func=function)

    Similar logic applies to lists.
    """

    _function_relationships = db.Column(db.PickleType)
    
    def __setattr__(self, name, value):
        """
        Convert value to Function model if setting a function relationship
        """
        if name == '_sa_instance_state':
            return super().__setattr__(name, value)
        function_relationships = self._function_relationships or []
        if name in function_relationships:
            relationship = inspect(self).mapper.relationships[name]
            model_class = relationship.mapper.class_
            if relationship.uselist:
                value = value if isinstance(value, list) else [value]
                value = self._to_function_models(value, model_class)
            else:
                value = self._to_function_model(value, model_class)
        return super().__setattr__(name, value)

    def _to_function_models(self, funcs, model_class):
        """Convert a list of functions to Function models"""
        models = [self._to_function_model(f, model_class) for f in funcs]
        return [m for m in models if m is not None]
    
    def _to_function_model(self, func, model_class):
        """Convert a single function to a Function model"""
        if isinstance(func, model_class):
            return func
        if callable(func):
            return model_class(self, func)
        if func is None:
            return None
        raise ValueError(
            'Function relationships requre Function models or callables'
        )

    def _set_function_relationships(self):
        """Find and store all function relationships
        
        Models which inherit from FunctionModelBase should call this 
        before function attributes are assigned.
        """
        relationships = inspect(self).mapper.relationships
        self._function_relationships = [
            r.key for r in relationships 
            if FunctionMixin in r.mapper.class_.__mro__
        ]