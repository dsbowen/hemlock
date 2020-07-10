"""# Navigation bar

Examples
--------
```python
from hemlock import Page, push_app_context
from hemlock.tools import Navbar, Navitem, Navitemdd, Dropdownitem

app = push_app_context()

url_root = 'https://dsbowen.github.io/'

navbar = Navbar(
\    'Hemlock', 
\    [
\        Navitem('Application', href=url_root+'app'),
\        Navitemdd(
\            'Tools', 
\            [
\                Dropdownitem('Language', href=url_root+'lang'),
\                Dropdownitem('Navbar', href=url_root+'navbar')
\           ]
\        )
\    ], 
\    href=url_root+'hemlock'
)

Page(navbar=navbar.render()).preview()
```
"""

from .random import key

from flask import request
from sqlalchemy_mutablesoup import SoupBase

import os
from copy import copy

DIR = os.path.dirname(os.path.realpath(__file__))

class NavBase():
    """
    All navigation models inherit from this base.

    Parameters
    ----------
    template : str
        Path to template file. This is *not* a Jinja template, as you may 
        wish to generate html for statics outside the application context.

    \*\*kwargs :
        Any attribute of navigation objects can be set by passing it as a 
        keyword argument.
    
    Attributes
    ----------
    a : bs4.Tag
        `<a>` tag.

    body : bs4.BeautifulSoup (sqlalchemy_mutablesoup.MutableSoup)
        Html container.

    label : str
        Navigation object label.

    href : str
        Hyperref associated with the object.
    """
    @property
    def a(self):
        return self.body.select_one('a')

    @property
    def label(self):
        return self.a.text

    @label.setter
    def label(self, val):
        self.body.set_element('a', val)

    @property
    def href(self):
        return self.a.attrs.get('href')

    @href.setter
    def href(self, val):
        self.a['href'] = val

    def __init__(self, template, **kwargs):
        self.id = 'navbar-'+key(10)
        self.body = SoupBase(
            open(template).read().format(self_=self), 'html.parser'
        )
        [setattr(self, key, val) for key, val in kwargs.items()]

    def is_active(self):
        """        
        Returns
        -------
        is_active : bool
            Indicates that the object's href is active.
        """
        try:
            return self.href == str(request.url_rule)
        except: # Exception will occur outside app context
            return False


class Navbar(NavBase):
    """
    Parameters
    ----------
    label : str, default=''
        Navbar brand.

    navitems : list of hemlock.tools.Navitem and hemlock.tools.Navitemdd
        Navigation items associated with the navbar.

    template : str, default='directory/navbar.html'
        By default, this is a file stored in the directory of the current 
        file.
    """
    def __init__(
            self, label='', navitems=[], 
            template=os.path.join(DIR, 'navbar.html'), **kwargs
        ):
        self.navitems = navitems
        super().__init__(template, label=label, **kwargs)

    def render(self):
        """
        Returns
        -------
        redered : bs4.BeautifulSoup
            A copy of `self.body` with rendered navitems.
        """
        body = copy(self.body)
        ul = body.select_one('ul')
        [ul.append(item.render()) for item in self.navitems]
        return body


class Navitem(NavBase):
    """
    Navigation item *without* dropdown items.

    Parameters
    ----------
    label : str, default=''

    template : str, default='directory/navitem.html'
        By default, this is a file stored in the directory of the current 
        file.
    """
    def __init__(
            self, label='', template=os.path.join(DIR, 'navitem.html'), 
            **kwargs
        ):
        super().__init__(template, label=label, **kwargs)

    def render(self):
        """
        Returns
        -------
        rendered : bs4.BeautifulSoup
            Copy of `self.body`.
        """
        body = copy(self.body)
        if self.is_active():
            li = body.select_one('li')
            if li.attrs.get('class') is None:
                li['class'] = []
            li['class'].append('active')
        return body


class Navitemdd(NavBase):
    """
    Navigation item *with* dropdown items.

    Parameters
    ----------
    label : str, default=''

    dropdownitems : list of hemlock.tools.Dropdownitem
    
    template : str, default='directory/navitemdd.html'
        By default, this is a file stored in the directory of the current 
        file.
    """
    def __init__(
            self, label='', dropdownitems=[], 
            template=os.path.join(DIR, 'navitemdd.html'), **kwargs
        ):
        self.dropdownitems = dropdownitems
        super().__init__(template, label=label, **kwargs)

    def render(self):
        """
        Returns
        -------
        rendered : bs4.BeautifulSoup
            A copy of `self.body` with rendered dropdown items.
        """
        body = copy(self.body)
        div = body.select_one('div.dropdown-menu')
        [div.append(item.render()) for item in self.dropdownitems]
        return body


class Dropdownitem(NavBase):
    """
    Parameters
    ----------
    label : str, default=''

    template : str, default='directory/dropdownitem.html'
        By default, this is a file stored in the directory of the current 
        file.
    """
    def __init__(
            self, label='', template=os.path.join(DIR, 'dropdownitem.html'), 
            **kwargs
        ):
        super().__init__(template, label=label, **kwargs)

    def render(self):
        """
        Returns
        -------
        rendered : bs4.BeautifulSoup
            Copy of `self.body`.
        """
        body = copy(self.body)
        if self.is_active():
            a = self.a
            if a.get('class') is None:
                a['class'] = []
            a['class'].append('active')
        return body