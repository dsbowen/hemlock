"""Base classes for public database models

Base is a generic base class for all Hemlock models. 

BranchingBase contains methods for growing and inserting new branches to a 
Participant's branch_stack. 

CompileBase contains convenience methods for models which compile html.

FunctionBase contains convenience methods for models with relationships to 
Function models.
"""

from hemlock.app import db
from hemlock.tools import CSS, JS

from bs4 import BeautifulSoup
from flask import current_app
from sqlalchemy import Column
from sqlalchemy.inspection import inspect
from sqlalchemy_mutable import MutableListType


class Base():
    @property
    def model_id(self):
        """ID for distinguishing models"""
        id = inspect(self).identity
        id = '-'.join([str(key) for key in id]) if id is not None else ''
        return type(self).__name__+'-'+str(id)
    
    def __init__(self, default_settings=[], **kwargs):
        """Add and flush all models on construction"""
        settings = {}
        [settings.update(self.app_settings(ds)) for ds in default_settings]
        settings.update(kwargs)
        [setattr(self, key, val) for key, val in settings.items()]
        db.session.add(self)
        db.session.flush([self])
        super().__init__()

    def app_settings(self, settings_name):
        if settings_name is not None and hasattr(current_app, settings_name):
            return getattr(current_app, settings_name)
        return {}
    
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
    css = Column(MutableListType)
    js = Column(MutableListType)

    @property
    def _css(self):
        return ''.join([
            sheet.render() if isinstance(sheet, CSS) else sheet
            for sheet in self.css
        ])

    @property
    def _js(self):
        return ' '.join([
            script.render() if isinstance(script, JS) else script
            for script in self.js
        ])

    def _prettify(self, html):
        """Prettify compiled html"""
        return BeautifulSoup(html, 'html.parser').prettify()
    
    def view_html(self, html=None):
        html = html or self._render()
        print(self._prettify(html))