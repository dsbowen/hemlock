"""Viewing page"""

from ...app import db

from bs4 import BeautifulSoup
from flask import request
from sqlalchemy_orderingitem import OrderingItem


class ViewingPage(OrderingItem, db.Model):
    """
    Stores HTML snapshot of each page for each participant. These can be 
    accessed in the researcher dashboard.

    Parameters
    ----------
    part : hemlock.Participant
        Participant to which this viewing page belongs.

    html : str
        HTML of the page.

    first_presentation : bool
        Indicates that this was the first time this page was presented to the 
        participant.

    Attributes
    ----------
    first_presentation : bool
        Set from the `first_presentation` parameter.

    html : str
        Set from the `html` parameter.

    index : str
        Order in which the participant saw this page.

    url_root : str
        URL root for viewing this page. This will be used to get absolute 
        paths to statics.

    Relationships
    -------------
    part : hemlock.Participant
        Set from the `part` parameter.
    """
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    first_presentation = db.Column(db.Boolean)
    html = db.Column(db.String)
    index = db.Column(db.Integer)
    url_root = db.Column(db.String)
    
    def __init__(self, part, html, first_presentation=True):
        self.part = part
        self.html = html
        self.first_presentation = first_presentation
        self.url_root = request.url_root

    def process(self):
        """
        Convert stylesheets and scripts from relative to absolute paths and 
        remove banner.
        """
        soup = BeautifulSoup(self.html, 'html.parser')
        self.convert_rel_paths(soup, 'href')
        self.convert_rel_paths(soup, 'src')
        banner = soup.select_one('span.banner')
        if banner is not None:
            banner.string = ''
        self.html = str(soup)

    def convert_rel_paths(self, soup, url_attr):
        """
        Convert relative to absolute path.

        Parameters
        ----------
        soup : bs4.BeautifulSoup
            Soup whose elements should be converted.

        url_attr : str
            URL attribute to convert.
        """
        elements = soup.select('[{}]'.format(url_attr))
        for e in elements:
            url = e.attrs.get(url_attr)
            if url is not None and url.startswith('/'):
                e.attrs[url_attr] = self.url_root + url