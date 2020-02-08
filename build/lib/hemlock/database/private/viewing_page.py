"""Viewing Page database model

Stores html snapshot of each Page for each Participant. These can be accessed
in the researcher dashboard.
"""

from hemlock.app import db

from bs4 import BeautifulSoup
from flask import request
from sqlalchemy_orderingitem import OrderingItem


class ViewingPage(OrderingItem, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    index = db.Column(db.Integer)
    html = db.Column(db.String)
    url_root = db.Column(db.String)
    
    def __init__(self, part, html):
        self.part = part
        self.html = html
        self.url_root = request.url_root

    def process(self):
        """Process HTML for viewing
        
        Convert stylesheets and scripts from relative to absolute paths and 
        remove icon.
        """
        soup = BeautifulSoup(self.html, 'html.parser')
        sheets = soup.select('link')
        [self.convert_to_abs_path(s, 'href') for s in sheets]
        scripts = soup.select('script')
        [self.convert_to_abs_path(s, 'src') for s in scripts]
        banner = soup.select_one('span.banner')
        if banner is not None:
            banner.string = ''
        self.html = str(soup)

    def convert_to_abs_path(self, element, url_attr):
        url = element.attrs.get(url_attr)
        if url is not None and url.startswith('/'):
            element.attrs[url_attr] = self.url_root + url