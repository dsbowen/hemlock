"""Select question"""

from hemlock.database.data.utils import *
from hemlock.database.choice import Option


class ChoiceQuestion(Question):
    choices = db.relationship(
        'Choice', 
        backref='question',
        order_by='Choice.index',
        collection_class=ordering_list('index'),
        foreign_keys='Choice._question_id'
    )

    @validates('choices')
    def validate_choice(self, key, val):
        assert isinstance(val, str) or isinstance(val, Choice)
        if isinstance(val, str):
            if type(self).__name__ in ['Select', 'MultiSelect']:
                return Option(label=val)
            return Choice(label=val)
        return val

    def _render(self):
        choice_wrapper = self.body.select_one('.choice-wrapper')
        [choice_wrapper.append(c._render()) for c in self.choices]
        return self.body

    def _record_response(self):
        if not self.multiple:
            response_id = request.form.get(self.model_id)
            self.response = Choice.query.get(response_id)
        else:
            response_ids = request.form.getlist(self.model_id)
            self.response = [Choice.query.get(id) for id in response_ids]

    def _record_data(self):
        if not self.multiple:
            self.data = None if self.response is None else self.response.value
        else:
            self.data = {
                c.value: int(c in self.response)
                for c in self.choices if c.value is not None
            }
    
    def _pack_data(self):
        var = self.var
        if not self.multiple or var is None:
            return super()._pack_data()
        if self.data is None:
            packed_data = {
                var+c.value:None for c in self.choices if c.value is not None
            }
        else:
            packed_data = {var+key: val for key, val in self.data.items()}
        return super()._pack_data(packed_data)        


class Select(InputGroup, ChoiceQuestion):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'select'}

    @Base.init('Select')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('select.html', q=self)
        return {'page': page, **kwargs}

    @property
    def select(self):
        return self.body.select_one('select#'+self.model_id)

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


class Check(ChoiceQuestion):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'check'}

    multiple = db.Column(db.Boolean, default=False)
    inline = db.Column(db.Boolean, default=False)

    @Base.init('Check')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('check.html', q=self)
        return {'page': page, **kwargs}
    
    @property
    def center(self):
        return 'text-center' in self.body.select_one('div.choice-wrapper')['class']

    @center.setter
    def center(self, val):
        assert isinstance(val, bool)
        if val == self.center:
            return
        choice_wrapper = self.body.select_one('div.choice-wrapper')
        if val:
            choice_wrapper['class'].append('text-center')
        else:
            choice_wrapper['class'].remove('text-center')
        self.body.changed()