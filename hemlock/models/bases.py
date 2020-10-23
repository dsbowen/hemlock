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
    [`sqlalchemy_function.FunctionRelator`](https://dsbowen.github.io/sqlalchemy-function/), 
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
    name = db.Column(db.String)

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

        if inspect(self).detached:
            self = self.__class__.query.get(self.id)
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
            data = {self.var: None if self.data is None else str(self.data)}
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


class HTMLMixin(Base):
    """
    Mixin for models which contribute html to a page.

    Parameters
    ----------
    template : str, default depends on object
        Jinja template which is rendered to produce `self.body`.

    extra_css : str or bs4.BeautifulSoup or list, default=''
        Extra stylesheets to append to the default css.

    extra_js : str or bs4.BeautifulSoup or list, default=''
        Extra scripts to append to the default javascript.

    Attributes
    ----------
    attrs : dict
        Most objects subclassing the `HTMLMixin` have a dictionary or html
        attributes for the main html tag of the `body`. For example, the 
        `Input` object's main tag is an `<input>` tag with attributes such as
        `type`, `min`, and `max`.

    body : sqlalchemy_mutablesoup.MutableSoupType
        The main html of the object.

    css : sqlalchemy_mutablesoup.MutableSoupType, default=''
        CSS the object contributes to the page.

    js : sqlalchemy_mutablesoup.MutableSoupType, default=''
        Javascript the object contributes to the page.

    Notes
    -----
    `HTMLMixin` also allows you to set attributes of the main html tag as if
    setting an attribute of the `HTMLMixin` object. For example, you can set 
    the `type` of the `<input>` tag of an `hemlock.Input` question with:

    ```python
    from hemlock import Input, push_app_context

    app = push_app_context()

    inpt = Input(type='number')
    inpt.body
    ```

    Out:

    ```
    ...
    <input class="form-control" id="input-1" name="input-1" type="number"/>
    ...
    ```

    Valid html attributes will vary depending on the object.
    """
    attrs = db.Column(HTMLAttrsType)
    template = db.Column(db.String)
    css = db.Column(MutableListJSONType)
    js = db.Column(MutableListJSONType)

    # HTML attribute names for the main tag
    _html_attr_names = []

    def __init__(
            self, template=None, attrs={}, 
            css=[], extra_css=[], js=[], extra_js=[], **kwargs
        ):
        def add_extra(attr, extra):
            # add extra css or javascript
            if extra:
                assert isinstance(extra, (str, list))
                if isinstance(extra, str):
                    attr.append(extra)
                else:
                    attr += extra

        db.session.add(self)
        db.session.flush([self])
        self.template = template
        self.attrs = attrs
        self.css, self.js = css, js
        add_extra(self.css, extra_css)
        add_extra(self.js, extra_js)
        super().__init__(**kwargs)

    def __getattribute__(self, key):
        if key == '_html_attr_names' or key not in self._html_attr_names:
            return super().__getattribute__(key)
        return self.attrs.get(key)

    def __setattr__(self, key, val):
        if key in self._html_attr_names:
            self.attrs[key] = val
        else:
            super().__setattr__(key, val)


class InputBase():
    """
    Base for models which contain `<input>` tags.

    Attributes
    ----------
    attrs : dict
        Input tag html attributes.
        
    input : bs4.Tag or None
        Input tag associated with this model.
    """
    _html_attr_names = [
        'type',
        'readonly',
        'disabled',
        'size',
        'maxlength',
        'max', 'min',
        'multiple',
        'pattern',
        'placeholder',
        'required',
        'step',
        'autofocus',
        'height', 'width',
        'list',
        'autocomplete',
    ]

    @property
    def attrs(self):
        return self.input.attrs

    @attrs.setter
    def attrs(self, val):
        self.input.attrs = val
        self.body.changed()

    @property
    def input(self):
        return self.body.select_one('#'+self.model_id)

    def input_from_driver(self, driver=None):
        """
        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.Webdriver
            Driver which will be used to select the input. Does not need to be Chrome.

        Returns
        -------
        input : selenium.webdriver.remote.webelement.WebElement
            Web element of the `<input>` tag associated with this model.
        """
        return driver.find_element_by_css_selector('#'+self.model_id)

    def label_from_driver(self, driver):
        """
        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.Webdriver
            Driver which will be used to select the label. Does not need to be Chrome.

        Returns
        -------
        label : selenium.webdriver.remote.webelement.WebElement
            Web element of the label tag associated with this model.
        """
        selector = 'label[for={}]'.format(self.model_id)
        return driver.find_element_by_css_selector(selector)