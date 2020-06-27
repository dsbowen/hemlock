"""# Navigation bar

See <https://dsbowen.github.io/sqlalchemy-nav>.
"""

from ..app import db
from .bases import Base

from flask import Markup
from sqlalchemy_nav import NavbarMixin, NavitemMixin, DropdownitemMixin 


class Navbar(NavbarMixin, Base, db.Model):
    """
    Navigation bar model.

    Interits from `sqlalchemy_nav.NavbarMixin`.

    Attributes
    ----------
    pages : list of hemlock.Page or None, default=None
        Pages on which the navbar will be displayed.
    """
    pages = db.relationship('Page', backref='navbar', lazy='dynamic')

    def render(self, body=None):
        """
        Parameters
        ----------
        body : bs4.BeautifulSoup or None, default=None
            Html body to render. If `None` render `self.body`.

        Returns
        -------
        html : markupsafe.Markup
            Rendered navbar for insertion into Jinja template.
        """
        return Markup(str(super().render(body)))
    

class Navitem(NavitemMixin, Base, db.Model):
    """
    Item in the navigation bar.

    Inherits from `sqlalchemy_nav.NavitemMixin`.
    """

    
class Dropdownitem(DropdownitemMixin, Base, db.Model):
    """
    Dropdown item in a navigation item.

    Inherits from `sqlalchemy_nav.DropdownitemMixin`.
    """