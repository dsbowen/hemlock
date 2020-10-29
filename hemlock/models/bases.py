"""# Common bases and mixins"""

from ..app import db
from .functions import Compile, Debug, Validate, Submit, Navigate

from bs4 import BeautifulSoup
from flask import current_app, render_template
from sqlalchemy import Column, inspect
from sqlalchemy_modelid import ModelIdBase
from sqlalchemy_mutable import (
    HTMLAttrsType, MutableType, MutableJSONType, MutableListType, 
    MutableListJSONType, MutableModelBase
)
from sqlalchemy_mutablesoup import MutableSoupType
from sqlalchemy_orderingitem import OrderingItem

import os


class Base(OrderingItem, ModelIdBase):
    """
    Base for all Hemlock models.

    Interits from  
    [`sqlalchemy_orderingitem.Orderingitem`](https://dsbowen.github.io/sqlalchemy-orderingitem/) and 
    [`sqlalchemy_modelid.ModelIdBase`](https://dsbowen.github.io/sqlalchemy-modelid/).

    Parameters
    ----------
    \*\*kwargs :
        You can set any attribute by passing it as a keyword argument.

    Attributes
    ----------
    name : str or None, default=None
        Used primarily as a filter for database querying.
    """
    def __init__(self, **kwargs):
        settings = current_app.settings.get(type(self).__name__)
        settings = settings.copy() if settings else {}
        settings.update(kwargs)
        [setattr(self, key, val) for key, val in settings.items()]
        super().__init__()


class BranchingBase(Base):
    navigate = db.Column(MutableType)

    def _eligible_to_insert_branch(self):
        """Indicate that object is eligible to grow and insert next branch
        
        A Page or Branch is eligible to insert the next branch to the
        Participant's branch_stack iff the navigator is not None and
        the next branch is not already in the branch_stack.
        """
        return (
            self.navigate is not None 
            and self.next_branch not in self.part.branch_stack
        )

    def _navigate(self):
        from .branch import Branch

        def set_relationships():
            self.next_branch = next_branch
            if isinstance(self, Branch):
                next_branch.origin_branch = self
                next_branch.origin_page = None
            else:
                # self is hemlock.Page
                next_branch.origin_branch = None
                next_branch.origin_page = self

        next_branch = self.navigate(self)
        assert isinstance(next_branch, Branch)
        set_relationships()
        next_branch.current_page = next_branch.start_page
        return self


class Data(Base, MutableModelBase, db.Model):
    """
    Polymorphic base for all objects which contribute data to the dataframe.

    Data elements 'pack' their data and return it to their participant, who in turn sends it to the data store.

    Attributes
    ----------
    data : sqlalchemy_mutable.MutableType, default=None
        Data this element contributes to the dataframe.

    data_rows : int, default=1
        Number of rows this data element contributes to the dataframe for its 
        participant. If negative, this data element will 'fill in' any emtpy
        rows at the end of the dataframe with its most recent value.

    index : int or None, default=None
        Order in which this data element appears in its parent; usually a 
        `hemlock.Branch`, `hemlock.Page`, or `hemlock.Question`.

    var : str or None, default=None
        Variable name associated with this data element. If `None`, the data 
        will not be recorded.

    record_order : bool, default=False
        Indicates that the order of this data element should be recorded in
        the datafame. The order is the order in which this element appeared
        relative to other elements with the same variable name.

    record_index : bool, default=False
        Indicates that the index of this data element should be recorded in
        the dataframe. The index is the order in which this element appeared
        relative to other elements with the same parent. For example, the
        index of a question is the order in which the question appeared on its
        page.

    record_choice_index : bool, default=False
        Indicates that the index of this data element's choices should be 
        recorded in the dataframe. For example, a `hemlock.Check` question has
        multiple choices that the participant can select. The index of a 
        choice is its index in the question's choice list.
    """
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'data',
        'polymorphic_on': data_type
    }

    data = db.Column(MutableJSONType)
    data_rows = db.Column(db.Integer, default=1)
    index = db.Column(db.Integer)
    var = db.Column(db.Text)
    record_order = db.Column(db.Boolean, default=False)
    record_index = db.Column(db.Boolean, default=False)
    record_choice_index = db.Column(db.Boolean, default=False)

    def _pack_data(self, data=None):
        """
        Pack data for storing in data store.

        Parameters
        ----------
        data : dict or None, default=None
            Partly packed data from a downstream class.

        Returns
        -------
        packed_data : dict
        
        Notes
        -----
        `var`Index is the index of the object; its order within its
        Branch, Page, or Question. `var`Order is the order of the data element
        relative to other data elements with the same variable.
        """
        if self.var is None:
            return {}
        if data is None:
            data = {self.var: None if self.data is None else self.data}
        if hasattr(self, 'order') and self.record_order:
            data[self.var+'Order'] = self.order
        if hasattr(self, 'index') and self.record_index:
            data[self.var+'Index'] = self.index
        if hasattr(self, 'choices') and self.record_choice_index:
            data.update({
                self.var+c.name+'Index': idx
                for idx, c in enumerate(self.choices) if c.name is not None
            })
        return data