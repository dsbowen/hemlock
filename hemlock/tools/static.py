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

    def get_url(self, offline=False):
        offline = offline or current_app.offline
        if not offline and self.cdn is not None:
            return self.cdn
        if self.filename is not None:
            bp = self.blueprint+'.' if self.blueprint is not None else ''
            return url_for(bp+'static', filename=self.filename)
        return ''

    def as_css(self, offline=False):
        return CSS.format(href=self.get_url(offline))

    def as_js(self, offline=False):
        return JS.format(src=self.get_url(offline))
        

CSS = '<link href="{href}" rel="stylesheet" type="text/css"/>'
JS = '<script src="{src}"></script>'