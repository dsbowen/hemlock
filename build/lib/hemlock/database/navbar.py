"""Navigation bar database model

A `Navbar` is associated with a `Page`, and is rendered in a 
Flask-Bootstrap4 Jinja template. See dsbowen.github.io/sqlalchemy-nav for 
more details.
"""

from hemlock.app import db
from hemlock.database.bases import Base

from flask import Markup
from sqlalchemy_nav import NavbarMixin, NavitemMixin, DropdownitemMixin 


class Navbar(NavbarMixin, Base, db.Model):
    pages = db.relationship('Page', backref='navbar', lazy='dynamic')

    @Base.init('Navbar')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, body=None):
        return Markup(str(super().render(body)))
    

class Navitem(NavitemMixin, Base, db.Model):
    @Base.init('Navitem')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
class Dropdownitem(DropdownitemMixin, Base, db.Model):
    @Base.init('Dropdownitem')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)