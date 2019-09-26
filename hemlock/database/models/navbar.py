"""Navigation bar database model"""

from hemlock.app import db
from hemlock.database.private import Base
from hemlock.database.types import MarkupType

from flask import Markup
from sqlalchemy.ext.orderinglist import ordering_list


class Navbar(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    pages = db.relationship('Page', backref='nav', lazy='dynamic')
    navitems = db.relationship(
        'Navitem',
        backref='nav',
        order_by='Navitem.index',
        collection_class=ordering_list('index')
        )
        
    brand = db.Column(MarkupType)
    url = db.Column(db.String)
    _type = db.Column(db.String)
    
    REGISTRATIONS = ['html_compiler']
    html_compiler = {}
    
    def __init__(self, navitems=[], pages=[], brand=None, type='default'):
        Base.__init__(self)
        self.navitems = navitems
        self.pages = pages
        self.brand = brand
        self.type = type


DEFAULT_NAVBAR = """
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        {brand}
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
                {navitems}
            </ul>
        </div>
    </nav>"""
        
BRAND = """
        <a class="navbar-brand" href="{url}">
        {brand}
        </a>"""

@Navbar.register(type='default', registration='html_compiler')
def default_compiler(navbar):
    url = navbar._get_url()
    brand = navbar.brand
    brand = '' if brand is None else BRAND.format(url=url, brand=brand)
    navitems = ''.join([i._compile_html() for i in navbar.navitems])
    return Markup(DEFAULT_NAVBAR.format(brand=brand, navitems=navitems))