"""Base classes for public database models

Base is a generic base class for all Hemlock models. 

BranchingBase contains methods for growing and inserting new branches to a 
Participant's branch_stack. 

CompileBase contains convenience methods for models which compile html.
"""

from hemlock.app import db

from bs4 import BeautifulSoup
from flask import Markup


class Base():
    @property
    def model_id(self):
        """ID for distinguishing models"""
        return type(self).__name__+'-'+str(self.id)
    
    def __init__(self, *args, **kwargs):
        """Add and flush all models on construction"""
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


class CompileBase(Base):
    def render(self, html=None):
        """Get and prettify compiled html
        
        CompileBase expects Models which inherit it to have a compile_html() method. The compile_html() method returns raw html.
        """
        html = self.compile_html() if html is None else html
        soup = BeautifulSoup(html, 'html.parser')
        return soup.prettify()
    
    def view_html(self, html=None):
        print(self.render(html))