"""Range question"""

from hemlock.qpolymorphs.utils import *


class Range(InputBase, Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'range'}

    @Question.init('Range')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('range.html', q=self)
        self.js = render_template('range.js', q=self)
        return {'page': page, **kwargs}

    @property
    def min(self):
        return self.input.attrs.get('min')

    @min.setter
    def min(self, val):
        self.input['min'] = val
        self.body.changed()

    @property
    def max(self):
        return self.input.attrs.get('max')

    @max.setter
    def max(self, val):
        self.input['max'] = val
        self.body.changed()

    @property
    def step(self):
        return self.input.attrs.get('step')

    @step.setter
    def step(self, val):
        self.input['step'] = val
        self.body.changed()