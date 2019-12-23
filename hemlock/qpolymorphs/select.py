"""Select question"""

from hemlock.qpolymorphs.utils import *


class Select(InputGroup, ChoiceQuestion):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'select'}

    @ChoiceQuestion.init('Select')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('select.html', q=self)
        return {'page': page, **kwargs}

    @property
    def select(self):
        return self.body.select_one('select#'+self.model_id)
    
    @property
    def rows(self):
        return self.select.attrs.get('rows')

    @rows.setter
    def rows(self, val):
        assert isinstance(val, int)
        self.select['rows'] = val
        self.body.changed()

    @property
    def multiple(self):
        return 'multiple' in self.select.attrs

    @multiple.setter
    def multiple(self, val):
        assert isinstance(val, bool)
        if val:
            self.select['multiple'] = None
        else:
            self.select.attrs.pop('multiple', None)
        self.body.changed()