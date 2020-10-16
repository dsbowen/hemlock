"""# Common bases and mixins"""

from ..app import db
from .functions import Compile, Debug, Validate, Submit, Navigate

from bs4 import BeautifulSoup
from flask import current_app, render_template
from sqlalchemy import Column, inspect
from sqlalchemy_function import FunctionRelator
from sqlalchemy_modelid import ModelIdBase
from sqlalchemy_mutable import MutableType, MutableListType, MutableModelBase
from sqlalchemy_mutablesoup import MutableSoupType
from sqlalchemy_orderingitem import OrderingItem

import os


class Base(FunctionRelator, OrderingItem, ModelIdBase):
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
        if self.id is None:
            db.session.add(self)
            db.session.flush([self])
        settings = current_app.settings.get(self.__class__.__name__)
        settings = settings.copy() if settings else {}
        settings.update(kwargs)
        [setattr(self, key, val) for key, val in settings.items()]
        super().__init__()


class BranchingBase(Base):
    _navigate_func = db.Column(MutableType)

    @property
    def navigate(self):
        return self._navigate_func

    @navigate.setter
    def navigate(self, func):
        if callable(func) and not isinstance(func, Navigate):
            func = Navigate(func)
        self._navigate_func = func

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
        if inspect(self).detached:
            self = self.__class__.query.get(self.id)
        self.navigate(self)
        return self


class PageLogicBase(Base):
    _compile_funcs = db.Column(MutableListType)

    @property
    def compile(self):
        return self._compile_funcs or []

    @compile.setter
    def compile(self, funcs):
        self._compile_funcs = self._function_setter(funcs, Compile)

    _debug_funcs = db.Column(MutableListType)

    @property
    def debug(self):
        return self._debug_funcs or []

    @debug.setter
    def debug(self, funcs):
        if os.environ.get('DEBUG_FUNCTIONS') != 'False':
            self._debug_funcs = self._function_setter(funcs, Debug)

    _validate_funcs = db.Column(MutableListType)

    @property
    def validate(self):
        return self._validate_funcs or []

    @validate.setter
    def validate(self, funcs):
        self._validate_funcs = self._function_setter(funcs, Validate)

    _submit = db.Column(MutableListType)

    @property
    def submit(self):
        return self._submit_funcs or []

    @submit.setter
    def submit(self, funcs):
        self._submit_funcs = self._function_setter(funcs, Submit)

    def _function_setter(self, funcs, func_cls):
        if not funcs:
            return []
        if not isinstance(funcs, list):
            funcs = [funcs]
        return [
            f if isinstance(f, func_cls) else func_cls(f) for f in funcs
        ]


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

    data = db.Column(MutableType)
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
    body = db.Column(MutableSoupType)
    css = db.Column(MutableSoupType, default='')
    js = db.Column(MutableSoupType, default='')

    # HTML attribute names for the main tag
    _html_attr_names = []

    @property
    def attrs(self):
        print('WARNING: attrs property not implemented')
        return

    @attrs.setter
    def attrs(self, val):
        print('WARNING: attrs property not implemented')
        return

    def __init__(self, template=None, extra_css='', extra_js='', **kwargs):
        db.session.add(self)
        db.session.flush([self])
        if template is not None:
            self.body = render_template(template, self_=self)
        if 'css' in kwargs:
            kwargs['css'] = self._join_soup(kwargs['css'])
        if 'js' in kwargs:
            kwargs['js'] = self._join_soup(kwargs['js'])
        super().__init__(**kwargs)
        self.css.append(self._join_soup(extra_css))
        self.css.changed()
        self.js.append(self._join_soup(extra_js))
        self.js.changed()

    def _join_soup(self, items):
        """
        Parameters
        ----------
        items : str or bs4.BeautifulSoup or list
            Items to join in a BeautifulSoup object.

        Returns
        -------
        soup : bs4.BeautifulSoup
        """
        items = [items] if isinstance(items, str) else items
        soup = BeautifulSoup('', 'html.parser')
        soup.extend([
            BeautifulSoup(i, 'html.parser') if isinstance(i, str) else i
            for i in items
        ])
        return soup

    def add_external_css(self, **attrs):
        """
        Parameters
        ----------
        \*\*attrs :
            Attribute names and values in the `<link/>` tag.

        Returns
        -------
        self : hemlock.HTMLMiixn

        Notes
        -----
        See (statics.md#hemlocktoolsexternal_css).
        """
        from ..tools import external_css
        self.css.append(BeautifulSoup(external_css(**attrs), 'html.parser'))
        self.css.changed()
        return self

    def add_internal_css(self, style):
        """
        Parameters
        ----------
        style : dict
            Maps css selector to an attributes dictionary. The attributes 
            dictionary maps attribute names to values.

        Returns
        -------
        self : hemlock.HTMLMixin

        Notes
        -----
        See (statics.md#hemlocktoolsinternal_css).
        """
        from ..tools import internal_css
        self.css.append(BeautifulSoup(internal_css(style), 'html.parser'))
        self.css.changed()
        return self

    def add_external_js(self, **attrs):
        """
        Parameters
        ----------
        \*\*attrs : 
            Attribute names and values in the `<script>` tag.

        Returns
        -------
        self : hemlock.HTMLMixin

        Notes
        -----
        See (statics.md#hemlocktoolsexternal_js).
        """
        from ..tools import external_js
        self.js.append(BeautifulSoup(external_js(**attrs), 'html.parser'))
        self.js.changed()
        return self

    def add_internal_js(self, js):
        """
        Parameters
        ----------
        js : str
            Javascript code.

        Returns
        -------
        self : hemlock.HTMLMixin

        Notes
        -----
        See (statics.md#hemlocktoolsinternal_js).
        """
        from ..tools import internal_js
        self.js.append(BeautifulSoup(internal_js(js), 'html.parser'))
        self.js.changed()
        return self

    def update_attrs(self, **kwargs):
        """
        Update html tag attributes.

        Parameters
        ----------
        \*\*kwargs :
            Keyword arguments map attribute names to values.
        """
        for key, val in kwargs.items():
            if isinstance(val, bool) or val is None:
                if val:
                    self.attrs[key] = None
                else:
                    self.attrs.pop(key, None)
            else:
                self.attrs[key] = val
        self.body.changed()
        return self

    def __getattribute__(self, key):
        if key == '_html_attr_names' or key not in self._html_attr_names:
            return super().__getattribute__(key)
        val = self.attrs.get(key)
        return val in self.attrs if val is None else val

    def __setattr__(self, key, val):
        if key in self._html_attr_names:
            self.update_attrs(**{key: val})
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