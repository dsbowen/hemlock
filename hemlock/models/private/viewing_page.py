"""Viewing page"""

from ...app import db

from bs4 import BeautifulSoup
from flask import request
from sqlalchemy_orderingitem import OrderingItem

import os
from tempfile import NamedTemporaryFile


class ViewingPage(OrderingItem, db.Model):
    """
    Stores HTML snapshot of each page for each participant. These can be 
    accessed in the researcher dashboard.

    Parameters
    ----------
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
    downloaded = db.Column(db.Boolean, default=False)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    first_presentation = db.Column(db.Boolean)
    html = db.Column(db.String)
    index = db.Column(db.Integer)
    url_root = db.Column(db.String)
    
    def __init__(self, html, first_presentation=True):
        self.html = html
        self.first_presentation = first_presentation
        self.url_root = request.url_root

    def mkstmp(self):
        """
        Returns
        -------
        path : str
            Path to temporary html file.
        """
        def convert_rel_paths():
            """
            Convert stylesheets and scripts from relative to absolute paths and 
            remove banner.
            """
            soup = BeautifulSoup(self.html, 'html.parser')
            convert_url_attr(soup, 'href')
            convert_url_attr(soup, 'src')
            banner = soup.select_one('#banner')
            if banner is not None:
                banner.extract()
            self.html = str(soup)

        def convert_url_attr(soup, url_attr):
            elements = soup.select('[{}]'.format(url_attr))
            for e in elements:
                url = e.attrs.get(url_attr)
                if url is not None and url.startswith('/'):
                    e.attrs[url_attr] = self.url_root + url

        if not self.downloaded:
            convert_rel_paths()
            self.downloaded = True # cache result
        with NamedTemporaryFile('w', suffix='.html', delete=False) as f:
            f.write(self.html)
            uri = f.name
        return uri