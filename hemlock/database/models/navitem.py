"""Navigation item database model"""

from hemlock.app import db
from hemlock.database.private import Base

from flask import request, url_for 


class Navitem(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _navbar_id = db.Column(db.Integer, db.ForeignKey('navbar.id'))
    index = db.Column(db.Integer)
    
    url = db.Column(db.String)
    label = db.Column(db.String)
    _type = db.Column(db.String)
    
    REGISTRATIONS = ['html_compiler']
    html_compiler = {}
    
    def __init__(
            self, nav=None, index=None, url=None, label=None, type='default'):
        Base.__init__(self)
        
        self.set_nav(nav, index)
        self.url = url
        self.label = label
        self.type = type
    
    def set_nav(self, nav, index=None):
        self._set_parent(nav, index, 'nav', 'navitems')


DEFAULT_NAVITEM = """
        <li class="nav-item {active}">
            <a class="nav-link" href="{url}">{label}</a>
        </li>"""

@Navitem.register(type='default', registration='html_compiler')
def default_compiler(navitem):
    url = navitem._get_url()
    try:
        url_rule = request.url_rule
    except: # Excpetion will be called when running in shell
        url_rule = None
    active = 'active' if url == url_rule else ''
    label = '' if navitem.label is None else navitem.label
    return DEFAULT_NAVITEM.format(active=active, url=url, label=label)

