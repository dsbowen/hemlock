"""# Common bases and mixins"""

from ..app import db

from bs4 import BeautifulSoup
from flask import current_app, render_template
from sqlalchemy import Column, inspect
from sqlalchemy_function import FunctionRelator
from sqlalchemy_modelid import ModelIdBase
from sqlalchemy_mutable import MutableType, MutableModelBase
from sqlalchemy_mutablesoup import MutableSoupType
from sqlalchemy_orderingitem import OrderingItem


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
        data = {self.var: self.data} if data is None else data
        data[self.var+'Order'] = self.order
        if self.index is not None:
            data[self.var+'Index'] = self.index
        if hasattr(self, 'choices'):
            data.update({
                self.var+c.name+'Index': c.index
                for c in self.choices if c.name is not None
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
    body : sqlalchemy_mutablesoup.MutableSoupType
        The main html of the object.

    css : sqlalchemy_mutablesoup.MutableSoupType, default=''
        CSS the object contributes to the page.

    js : sqlalchemy_mutablesoup.MutableSoupType, default=''
        Javascript the object contributes to the page.
    """
    body = db.Column(MutableSoupType)
    css = db.Column(MutableSoupType, default='')
    js = db.Column(MutableSoupType, default='')

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


class InputBase():
    """
    Base for models which contain `<input>` tags.

    Attributes
    ----------
    input : bs4.Tag or None
        Input tag associated with this model.
    """
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