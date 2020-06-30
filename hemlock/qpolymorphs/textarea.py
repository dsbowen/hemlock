"""Textarea"""

from ..app import settings
from ..functions.debug import random_keys
from .utils import *

settings['Textarea'] = {'debug_functions': random_keys}


class Textarea(InputGroup, Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'textarea'}

    def __init__(self, page=None, template='textarea.html', **kwargs):
        self.body = render_template(template, q=self)
        self.js = render_template('textarea.js', q=self)
        super().__init__(page, **kwargs)

    @property
    def textarea(self):
        return self.body.select_one('textarea#'+self.model_id)

    def textarea_from_driver(self, driver):
        """Get textarea from driver for debugging"""
        return driver.find_element_by_css_selector('textarea#'+self.model_id)

    @property
    def rows(self):
        return self.textarea.attrs.get('rows')

    @rows.setter
    def rows(self, val):
        assert isinstance(val, int)
        self.textarea['rows'] = val
        self.body.changed()

    def _render(self, body=None):
        body = body or self.body.copy()
        textarea = body.select_one('#'+self.model_id)
        textarea.string = self.response or self.default or ''
        return super()._render(body)

    