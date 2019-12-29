
from hemlock.app import Settings, db
from hemlock.database.bases import Base, HTMLMixin
from hemlock.database.data import Data
from hemlock.database.choice import Choice, Option

from flask import request
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy_mutable import MutableType, MutableModelBase

from copy import copy

@Settings.register('Question')
def settings():
    return {'css': '', 'js': ''}


class Question(Data, HTMLMixin, MutableModelBase):
    id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
    question_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'polymorphic_on': question_type
    }

    @property
    def part(self):
        return None if self.page is None else self.page.part

    """Relationships to Function models"""
    compile_functions = db.relationship(
        'Compile',
        backref='question',
        order_by='Compile.index',
        collection_class=ordering_list('index')
    )

    validate_functions = db.relationship(
        'Validate', 
        backref='question', 
        order_by='Validate.index',
        collection_class=ordering_list('index')
    )
    
    submit_functions = db.relationship(
        'Submit',
        backref='question',
        order_by='Submit.index',
        collection_class=ordering_list('index')
    )

    debug_functions = db.relationship(
        'Debug',
        backref='question',
        order_by='Debug.index',
        collection_class=ordering_list('index')
    )

    default = db.Column(MutableType)
    response = db.Column(MutableType)

    @Data.init('Question')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        return {'page': page, **kwargs}

    """Shortcuts for modifying soup"""
    @property
    def error(self):
        return self.text('.error-txt')

    @error.setter
    def error(self, val):
        form_grp_cls = self.body.select_one('div.form-group')['class']
        if not val:
            try:
                form_grp_cls.remove('error')
            except:
                pass
        elif 'error' not in form_grp_cls:
            form_grp_cls.append('error')
        self._set_element((val or ''), parent_selector='span.error-txt')
        self.body.changed()

    @property
    def label(self):
        return self.text('.label-txt')

    @label.setter
    def label(self, val):
        self._set_element((val or ''), parent_selector='.label-txt')
        self.body.changed()

    def clear_error(self):
        self.error = None

    def clear_response(self):
        self.response = None

    """Methods executed during study"""
    def _compile(self):
        [compile_func() for compile_func in self.compile_functions]

    def _render(self, body=None):
        return body or self.body.copy()

    def _record_response(self):
        self.response = request.form.get(self.model_id)
        
    def _validate(self):
        """Validate Participant response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        for validate_func in self.validate_functions:
            error = validate_func()
            if error:
                self.error = error
                return False
        self.error = None
        return True

    def _record_data(self):
        self.data = self.response
    
    def _submit(self):
        [submit_func() for submit_func in self.submit_functions]

    def _debug(self, driver):
        [debug_func(driver) for debug_func in self.debug_functions]


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
        if isinstance(val, Choice):
            return val
        val = str(val)
        if type(self).__name__ == 'Select':
            return Option(label=val)
        return Choice(label=val)

    @Question.init('ChoiceQuestion')
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def _render(self, body=None):
        body = body or self.body.copy()
        choice_wrapper = self._choice_wrapper(body)
        [choice_wrapper.append(c._render()) for c in self.choices]
        return body
    
    def _choice_wrapper(self, body=None):
        return (body or self.body).select_one('.choice-wrapper')

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
        elif isinstance(self.data, dict):
            packed_data = {var+key: val for key, val in self.data.items()}
        else:
            packed_data = self.data
        return super()._pack_data(packed_data)