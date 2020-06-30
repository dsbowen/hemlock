"""Input question"""

from ..app import settings
from ..functions.debug import send_datetime, random_keys
from .utils import *

from datetime_selenium import get_datetime

from datetime import datetime

html_datetime_types = (
    'date',
    'datetime-local',
    'month',
    'time',
    'week',
)

def debug_func(driver, question):
    if question.input_type in html_datetime_types:
        send_datetime(driver, question)
    else:
        random_keys(driver, question)

settings['Input'] = {'debug_functions': debug_func}


class Input(InputGroup, InputBase, Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'input'}

    @Question.init('Input')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('input.html', q=self)
        return {'page': page, **kwargs}

    @property
    def input_type(self):
        return self.input.get('type')

    @input_type.setter
    def input_type(self, val):
        self.input['type'] = val
        self.body.changed()

    def _submit(self, *args, **kwargs):
        """Convert data to `datetime` object if applicable"""
        if self.input_type in html_datetime_types:
            self.data = get_datetime(self.response) or None
        return super()._submit(*args, **kwargs)