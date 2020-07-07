"""# Common bases and mixins"""

from ..app import db

from bs4 import BeautifulSoup
from flask import current_app, render_template
from sqlalchemy import Column
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
            self.navigate_function is not None 
            and self.next_branch not in self.part.branch_stack
        )

    def _navigate(self):
        self.navigate_function(self)
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

    Attributes
    ----------
    body : sqlalchemy_mutablesoup.MutableSoupType
        The main html of the object.

    css : sqlalchemy_mutablesoup.MutableSoupType, default=None
        CSS the object contributes to the page.

    js : sqlalchemy_mutablesoup.MutableSoupType, default=None
        Javascript the object contributes to the page.
    """
    body = db.Column(MutableSoupType)
    css = db.Column(MutableSoupType)
    js = db.Column(MutableSoupType)

    def __init__(self, template=None, **kwargs):
        db.session.add(self)
        db.session.flush([self])
        if template is not None:
            self.body = render_template(template, self_=self)
        super().__init__(**kwargs)

    def add_external_css(self, **attrs):
        """
        Add external css to `self.css`. The external css is a `<link>` tag
        with the specified attributes. In particular, specify the `href`
        attribute.

        Parameters
        ----------
        \*\*attrs :
            Attribute names and values in the `<link>` tag.

        Returns
        -------
        self : hemlock.HTMLMiixn
        """
        self._update_col(
            col=self.css,
            template='<link {}/>',
            attrs={'rel': 'stylesheet', 'type': 'text/css'},
            input_attrs=attrs
        )
        return self

    def add_external_js(self, **attrs):
        """
        Add external javascript to `self.js`. The external js is a `<script>`
        tag with the specified attributes. In particular, specify the `src`
        attribute.

        Parameters
        ----------
        \*\*attrs : 
            Attribute names and values in the `<script>` tag.

        Returns
        -------
        self : hemlock.HTMLMixin
        """
        self._update_col(
            col=self.js,
            template='<script {}></script>',
            attrs={},
            input_attrs=attrs
        )
        return self

    def _update_col(self, col, template, attrs, input_attrs):
        """Update a `Column` (self.css or self.js)

        This method beings by translating the default attributes, `attrs`, 
        and the user input attributes, `input_attrs` into HTML format. It 
        then inserts the formatted attributes into an HTML `template`. 
        Finally, it updates the column, `col`.
        """
        attrs.update(input_attrs)
        html_attrs = ' '.join([key+'="'+val+'"' for key,val in attrs.items()])
        html = template.format(html_attrs)
        col.append(BeautifulSoup(html, 'html.parser'))
        col.changed()
    
    def add_internal_css(self, style):
        """
        Add internal css to `self.css`. The internal css is a `<style>` tag
        with the specified css selector : style dictionary.

        Parameters
        ----------
        style : dict
            Maps css selector to a style dictionary. The style dictionary maps
            attribute names to values.

        Returns
        -------
        self : hemlock.HTMLMixin
        """
        css = ' '.join(
            [self._format_style(key, val) for key, val in style.items()]
        )
        html = '<style>{}</style>'.format(css)
        self.css.append(BeautifulSoup(html, 'html.parser'))
        self.css.changed()
        return self
            
    def _format_style(self, selector, attrs):
        """`attrs` maps attribute names to values"""
        attrs = ' '.join([key+':'+val+';' for key, val in attrs.items()])
        return selector+' {'+attrs+'}'

    def add_internal_js(self, js):
        """
        Add internal javascript to `self.js`. The interal js is a `<script>`
        tag with the specified `js` code.

        Parameters
        ----------
        js : str
            Javascript code.

        Returns
        -------
        self : hemlock.HTMLMixin
        """
        if not js.startswith('<script>'):
            js = '<script>{}</script>'.format(js)
        self.js.append(BeautifulSoup(js, 'html.parser'))
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