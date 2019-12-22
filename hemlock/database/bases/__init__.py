"""Base classes for public database models

Base is a generic base class for all Hemlock models. 

BranchingBase contains methods for growing and inserting new branches to a 
Participant's branch_stack. 

HTMLMixin contains convenience methods for models which manipulate HTML.
"""

from hemlock.app import Settings, db
from hemlock.database.types import MutableSoupType
from hemlock.tools import CSS, JS

from bs4 import BeautifulSoup
from flask import render_template
from sqlalchemy import Column
from sqlalchemy.inspection import inspect
from sqlalchemy_function import FunctionRelator
from sqlalchemy_orderingitem import OrderingItem


class Base(FunctionRelator, OrderingItem):
    @property
    def model_id(self):
        """ID for distinguishing models"""
        id = inspect(self).identity
        id = '-'.join([str(key) for key in id]) if id is not None else ''
        return type(self).__name__+'-'+str(id)

    def init(*settings_keys):
        """Decorator for initialization function

        The decorator wraps __init__ as follows:
        1. Add and flush object to database
        2. Execute __init__
        3. Apply settings

        The wrapper derives settings first from settings keys, which are
        passed to the decorator. Secondly, the __init__ function may return a
        dictionary of attribute:value mappings to apply, which override 
        default settings.
        """
        settings_keys = list(settings_keys)
        settings_keys.reverse()
        def wrapper(init_func):
            def inner(self, *args, **kwargs):
                db.session.add(self)
                db.session.flush([self])
                settings = Settings.get(*settings_keys)
                attrs = init_func(self, *args, **kwargs)
                if attrs is not None:
                    settings.update(attrs)
                [setattr(self, key, val) for key, val in settings.items()]
                return
            return inner
        return wrapper


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


class HTMLMixin(Base):
    css = Column(MutableSoupType)
    js = Column(MutableSoupType)
    body = Column(MutableSoupType)

    def text(self, selector, parent=None):
        elem = self.body.select_one(selector, parent)
        return None if elem is None else elem.text

    def _set_element(
            self, val, parent_selector, target_selector=None, 
            gen_target=None, args=[], kwargs={}
        ):
        """Set a soup element
        
        `parent_selector` selects an ancestor of the target from the body. 
        The target is then selected as a descendent of the parent. Its 
        value is set to the input value.
        """
        parent = self.body.select_one(parent_selector)
        if not val:
            return parent.clear()
        target = self._get_target(
            parent, target_selector, gen_target, args, kwargs
        )
        if isinstance(val, str):
            val = BeautifulSoup(val, 'html.parser')
        target.clear()
        target.append(val)
        self.body.changed()

    def _get_target(self, parent, target_selector, gen_target, args, kwargs):
        """Get target element

        If `target_selector` is None, the target attribute is assumed to be 
        the parent attribute. Otherwise, the target is assumed to be a 
        descendent of the parent. If the target does not yet exist, generate 
        a child Tag which includes the target.
        """
        if target_selector is None:
            return parent
        target = parent.select_one(target_selector)
        if target is not None:
            return target
        parent.append(gen_target(*args, **kwargs))
        return parent.select_one(target_selector)