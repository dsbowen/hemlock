"""Static tool

Statics return a url for a static file, given the filename and (optionally)
the blueprint to which it belongs.
"""

from flask import Markup, current_app, url_for
from sqlalchemy_mutable import Mutable

class Static(Mutable):
    def __init__(self, cdn=None, filename=None, blueprint=None):
        self.cdn = cdn
        self.filename = filename
        self.blueprint = blueprint

    def get_url(self):
        assert self.cdn is not None or self.filename is not None
        if not current_app.offline and self.cdn is not None:
            return self.cdn
        bp = self.blueprint+'.' if self.blueprint is not None else ''
        return url_for(bp+'static', filename=self.filename)

    def as_css(self):
        return CSS.format(href=self.get_url())

    def as_js(self):
        return JS.format(src=self.get_url())
        

CSS = '<link href="{href}" rel="stylesheet" type="text/css"/>'
JS = '<script src="{src}"></script>'