"""Base classes for public database models

Base is a generic base class for all Hemlock models. 

BranchingBase contains methods for growing and inserting new branches to a 
Participant's branch_stack. 

CompileBase contains convenience methods for models which compile html.
"""

from hemlock.app import Settings, db
from hemlock.database.types import MutableSoupType
from hemlock.tools import CSS, JS

from bs4 import BeautifulSoup
from flask import current_app
from sqlalchemy import Column
from sqlalchemy.inspection import inspect
from sqlalchemy_function import FunctionRelator
from sqlalchemy_mutable import MutableListType
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


class HTMLBase(Base):
    css = Column(MutableSoupType)
    js = Column(MutableSoupType)
    soup = Column(MutableSoupType)

    def select(self, selector, parent=None):
        elem = self.select_all(selector, parent)
        if elem:
            return elem[0]

    def select_all(self, selector, parent=None):
        return (parent or self.soup).select(selector)

    def text(self, selector, parent=None):
        elem = self.select(selector, parent)
        return None if elem is None else elem.text