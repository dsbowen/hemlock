
from hemlock.qpolymorphs.utils import *

from random import randint
from string import ascii_letters, digits


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