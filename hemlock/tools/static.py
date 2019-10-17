"""Static tool

Statics return a url for a static file, given the filename and (optionally)
the blueprint to which it belongs.
"""

from flask import Markup, url_for
from sqlalchemy_mutable import Mutable

class Static(Mutable):
    def __init__(self, filename=None, blueprint=None):
        self.filename = filename
        self.blueprint = blueprint

    def _render(self):
        blueprint = '' if self.blueprint is None else self.blueprint+'.'
        return url_for(blueprint+'static', filename=self.filename)

def render_css(page):
    hrefs = get_urls(page.css)
    return Markup(' '.join([CSS.format(href=href) for href in hrefs]))

def render_js(page):
    srcs = get_urls(page.js)
    return Markup(' '.join([JS.format(src=src) for src in srcs]))

def get_urls(items):
    return [i._render() if isinstance(i, Static) else i for i in items]

CSS = '<link href="{href}" rel="stylesheet" type="text/css"/>'
JS = '<script src="{src}"></script>'