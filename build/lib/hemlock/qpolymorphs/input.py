"""Input question"""

from hemlock.qpolymorphs.utils import *

from datetime import datetime

# Mapping of datetime input types to formats
type_to_format = {
    'date': '%Y-%m-%d',
    'datetime-local': '%Y-%m-%dT%H:%M',
    'month': '%Y-%m',
    'time': '%H:%M',
    'week': '%Y-W%W'
}


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
        datetime_format = type_to_format.get(self.input_type)
        if datetime_format is not None:
            try: # will succeed if response is filled in
                self.data = datetime.strptime(self.response, datetime_format)
            except:
                pass
        return super()._submit(*args, **kwargs)