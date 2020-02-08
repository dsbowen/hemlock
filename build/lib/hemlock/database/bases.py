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
    name = db.Column(db.String)

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

    def add_external_css(self, **input_attrs):
        """`input_attrs` maps attribute to value in <link/> tag"""
        self._update_col(
            col=self.css,
            template='<link {}/>',
            attrs={'rel': 'stylesheet', 'type': 'text/css'},
            input_attrs=input_attrs
        )

    def add_external_js(self, **input_attrs):
        """`input_attrs` maps attibute to value in <script> tag"""
        self._update_col(
            col=self.js,
            template='<script {}></script>',
            attrs={},
            input_attrs=input_attrs
        )
    
    def add_internal_css(self, style):
        """`style` maps css selectors to a dictionary of style attributes"""
        css = ' '.join(
            [self._format_style(key, val) for key, val in style.items()]
        )
        html = '<style>{}</style>'.format(css)
        self.css.append(BeautifulSoup(html, 'html.parser'))
        self.css.changed()
            
    def _format_style(self, selector, attrs):
        """`attrs` maps attribute names to values"""
        attrs = ' '.join([key+':'+val+';' for key, val in attrs.items()])
        return selector+' {'+attrs+'}'

    def add_internal_js(self, js):
        """`js` is a string of Javascript code"""
        if not js.startswith('<script>'):
            js = '<script>{}</script>'.format(js)
        self.js.append(BeautifulSoup(js, 'html.parser'))
        self.js.changed()


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