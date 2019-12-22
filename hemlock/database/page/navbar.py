"""Navigation bar database model"""

from hemlock.app import db
from hemlock.database.bases import Base

from sqlalchemy_nav import BrandMixin, DropdownitemMixin, NavbarMixin, NavitemMixin


class Navbar(NavbarMixin, Base, db.Model):
    pages = db.relationship('Page', backref='nav', lazy='dynamic')

class Brand(BrandMixin, Base, db.Model):
    pass
    
class Navitem(NavitemMixin, Base, db.Model):
    pass
    
class Dropdownitem(DropdownitemMixin, Base, db.Model):
    pass