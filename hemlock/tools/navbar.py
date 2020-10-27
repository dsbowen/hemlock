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

# TODO use ConvertedList to enable this syntax

# navitems=[
#     ('Participant status', '/status'),
#     (
#         'Dropdown', 
#         [
#             ('Status', '/status'),
#             ('Logout', '/logout')
#         ]
#     ),
#     ('Download', '/download'),
#     ('Logout', '/logout')
# ]

from .random import key
from .statics import format_attrs

from convert_list import ConvertList
from flask import request

import os
from copy import copy, deepcopy

DIR = os.path.dirname(os.path.realpath(__file__))

class NavBase():
    """
    All navigation models inherit from this base.

    Parameters and attributes
    -------------------------
    label : str
        Label for the navigation element.

    template : str
        Path to template file or string. This is *not* a Jinja template, as 
        you may wish to generate html for statics outside the application 
        context.

    href : str, default=''
        Hyperref to which the navigation element links.

    a_attrs : dict, default={}
        Dictionary of HTML attributes for the navigation element's `<a>` tag.
    """
    @property
    def href(self):
        return self.a_attrs.get('href')

    @href.setter
    def href(self, val):
        self.a_attrs['href'] = val

    def __init__(self, label, template, href='', a_class=[], a_attrs={}):
        self.id = 'navbar-'+key(10)
        self.label = label
        self.template = (
            open(template).read() if os.path.exists(template)
            else template # assume template is string
        )
        self.a_class = a_class.copy()
        self.a_attrs = deepcopy(a_attrs)
        self.href = href

    def render(self):
        """
        Returns
        -------
        rendered : str
        """
        return self.template.format(self=self, a_attrs=self._render_attrs())

    def _render_attrs(self):
        a_class = self.a_class.copy()
        if self.href == str(request.url_rule):
            a_class.append('active')
        return format_attrs(**{'class': a_class}, **self.a_attrs)


class NavitemList(ConvertList):
    @classmethod
    def convert(cls, item):
        if isinstance(item, (Navitem, Navitemdd)):
            return item
        # item is tuple (label, href) if Navitem 
        # or (label, [dropdownitems]) if Navitemdd
        if isinstance(item[1], str):
            return Navitem(label=item[0], href=item[1])
        if isinstance(item[1], list):
            return Navitemdd(label=item[0], dropdownitems=item[1])
        raise ValueError('Incorrect value for navitem')


class Navbar(NavBase):
    """
    Parameters
    ----------
    label : str, default=''

    navitems : list of hemlock.tools.Navitem and hemlock.tools.Navitemdd
        Navigation items associated with the navbar.

    href : str, default=''

    template : str, default='directory/navbar.html'
        By default, this is a file stored in the directory of the current 
        file.

    a_attrs : dict

    navbar_attrs : dict
        HTML attributes for the `<nav>` tag.
    """
    @property
    def navitems(self):
        return self._navitems

    @navitems.setter
    def navitems(self, items):
        self._navitems = NavitemList(items)

    def __init__(
            self, label='', navitems=[], href='#',
            template=os.path.join(DIR, 'navbar.html'), 
            a_class=['navbar-brand'], a_attrs={},
            navbar_attrs={
                'class': [
                    'navbar', 
                    'navbar-expand-lg', 
                    'navbar-light', 
                    'bg-light', 
                    'fixed-top'
                ]
            }
        ):
        super().__init__(label, template, href, a_class, a_attrs)
        self.navitems = navitems
        self.navbar_attrs = deepcopy(navbar_attrs)

    def render(self):
        """
        Returns
        -------
        rendered : str
            Rendered navbar HTML.
        """
        return self.template.format(
            self=self,
            navbar_attrs=format_attrs(**self.navbar_attrs),
            a_attrs=self._render_attrs(),
            navitems='\n'.join([item.render() for item in self.navitems])
        )


class Navitem(NavBase):
    """
    Navigation item *without* dropdown items.

    Parameters
    ----------
    label : str, default=''

    href : str, default=''

    template : str, default='directory/navitem.html'
        By default, this is a file stored in the directory of the current 
        file.

    a_attrs : dict
    
    navitem_attrs : dict
        HTML attributes for the `navitem` div.
    """
    def __init__(
            self, label='', href='',
            template=os.path.join(DIR, 'navitem.html'), 
            a_class=['nav-item', 'nav-link'], a_attrs={}
        ):
        super().__init__(label, template, href, a_class, a_attrs)


class DropdownitemList(ConvertList):
    @classmethod
    def convert(cls, item):
        if isinstance(item, Dropdownitem):
            return item
        # item is tuple (label, href)
        if isinstance(item, tuple):
            return Dropdownitem(label=item[0], href=item[1])
        raise ValueError('Incorrect value for dropdown item')


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

    a_attrs : dict

    navitem_attrs : dict
        HTML attributes for the `navitem` div.
    """
    @property
    def dropdownitems(self):
        return self._dropdownitems

    @dropdownitems.setter
    def dropdownitems(self, items):
        self._dropdownitems = DropdownitemList(items)

    def __init__(
            self, label='', dropdownitems=[], 
            template=os.path.join(DIR, 'navitemdd.html'),
            a_class=['nav-item', 'nav-link', 'dropdown', 'dropdown-toggle'],
            a_attrs={
                'role': 'button',
                'data-toggle': 'dropdown',
                'aria-haspopup': 'true',
                'aria-expanded': 'false'
            },
            navitem_attrs={'class': ['nav-item', 'dropdown']}
        ):
        # note: href should not be passed
        super().__init__(label, template, a_class=a_class, a_attrs=a_attrs)
        self.dropdownitems = dropdownitems

    def render(self):
        """
        Returns
        -------
        rendered : str
        """
        return self.template.format(
            self=self,
            a_attrs=self._render_attrs(),
            items='\n'.join([item.render() for item in self.dropdownitems])
        )


class Dropdownitem(NavBase):
    """
    Parameters
    ----------
    label : str, default=''

    href : str, default=''

    template : str, default='directory/dropdownitem.html'
        By default, this is a file stored in the directory of the current 
        file.

    a_attrs : dict
    """
    def __init__(
            self, label='', href='',
            template=os.path.join(DIR, 'dropdownitem.html'),
            a_class=['dropdown-item'], a_attrs={}
        ):
        super().__init__(label, template, href, a_class, a_attrs)