
from hemlock.qpolymorphs.utils import *


class Textarea(InputGroup, Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'textarea'}

    @Question.init('Textarea')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('textarea.html', q=self)
        self.js = render_template('textarea.js', q=self)
        return {'page': page, **kwargs}

    @property
    def textarea(self):
        return self.body.select_one('textarea#'+self.model_id)

    @property
    def size(self):
        return self.textarea.attrs.get('size')

    @size.setter
    def size(self, val):
        assert isinstance(val, int)
        self.textarea['size'] = val
        self.body.changed()

    def _render(self):
        self.textarea.string = self.response or self.default or ''
        return self.body

    