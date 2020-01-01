"""Base classes for public database models

`Base` is a generic base class for all Hemlock models. It defines an `init` 
decorator for `__init__` methods of Hemlock models. 

`BranchingBase` defines a method which determines whether the branching 
object is eligible to insert its next branch into a `Participant`'s branch 
stack. 

`HTMLMixin` contains `css`, `js`, and `body` `MutableSoup` columns. This is 
subclassed by objects which contribute HTML to a suvey page.

`InputBase` defines convenience methods for objects whose `body` is an 
`input` Tag (e.g. `Input` and `Choice` objects).
"""

from hemlock.app import Settings, db

from bs4 import BeautifulSoup
from flask import render_template
from sqlalchemy import Column
from sqlalchemy_function import FunctionRelator
from sqlalchemy_modelid import ModelIdBase
from sqlalchemy_mutablesoup import MutableSoupType
from sqlalchemy_orderingitem import OrderingItem


class Base(FunctionRelator, OrderingItem, ModelIdBase):
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
    body = db.Column(MutableSoupType)
    css = db.Column(MutableSoupType)
    js = db.Column(MutableSoupType)


class InputBase():
    @property
    def input(self):
        return self.body.select_one('#'+self.model_id)

    def input_from_driver(self, driver=None):
        """Get input from driver for debugging"""
        return driver.find_element_by_css_selector('#'+self.model_id)

    def label_from_driver(self, driver):
        """Get label from driver for debugging"""
        selector = 'label[for={}]'.format(self.model_id)
        return driver.find_element_by_css_selector(selector)

    def _render(self, body=None):
        """Set the default value before rendering"""
        body = body or self.body.copy()
        inpt = body.select_one('#'+self.model_id)
        if inpt is not None:
            value = self.response or self.default
            if value is None:
                inpt.attrs.pop('value', None)
            else:
                inpt['value'] = value
        return super()._render(body)