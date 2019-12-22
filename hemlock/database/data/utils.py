"""Data element imports"""

from hemlock.app import Settings, db
from hemlock.database.bases import Base, HTMLMixin

from bs4 import Tag
from flask import render_template, request
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import MutableType, MutableModelBase

from random import choice, random


class Data(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'data',
        'polymorphic_on': data_type
    }

    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    all_rows = db.Column(db.Boolean)
    data = db.Column(MutableType)
    index = db.Column(db.Integer)
    order = db.Column(db.Integer)
    var = db.Column(db.Text)

    def _pack_data(self, data=None):
        """Pack data for storing in DataStore
        
        Note: `var`Index is the index of the object; its order within its
        Branch, Page, or Question. `var`Order is the order of the Question
        relative to other Questions with the same variable.
        
        The optional `data` argument is prepacked data from the element.
        """
        if self.var is None:
            return {}
        data = {self.var: self.data} if data is None else data
        if not self.all_rows:
            data[self.var+'Order'] = self.order
        if self.index is not None:
            data[self.var+'Index'] = self.index
        if hasattr(self, 'choices'):
            for c in self.choices:
                if c.name is not None:
                    data[self.var + c.name + 'Index'] = c.index
        return data


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
            form_grp_cls.remove('error')
        elif 'error' not in form_grp_cls:
            form_grp_cls.append('error')
        self._set_element((val or ''), parent_selector='span.error-txt')
        self.body.changed()

    @property
    def label(self):
        return self.text('.label-txt')

    @label.setter
    def label(self, val):
        self._set_element((val or ''), parent_selector='span.label-txt')
        self.body.changed()

    """Methods executed during study"""
    def _compile(self):
        [compile_fn() for compile_fn in self.compile_functions]

    def _render(self):
        return self.body

    def _record_response(self):
        self.response = request.form.get(self.model_id) or None
        
    def _validate(self):
        """Validate Participant response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        for validate_fn in self.validate_functions:
            self.error = validate_fn()
            if self.error is not None:
                return False
        return True

    def _record_data(self):
        self.data = self.response
    
    def _submit(self):
        [submit_fn() for submit_fn in self.submit_functions]

    def _debug(self, driver):
        [debug_fn(driver) for debug_fn in self.debug_functions]


class InputBase(Question):
    default = db.Column(MutableType)
    response = db.Column(MutableType)

    @property
    def input(self):
        return self.body.select_one('#'+self.model_id)

    def get_input_from_driver(self, driver=None):
        """Get input from driver for debugging"""
        return driver.find_element_by_css_selector('#'+self.model_id)

    def _render(self):
        """Set the default value before rendering"""
        value = self.response or self.default
        inpt = self.input
        if inpt.name == 'textarea':
            inpt.string = value or ''
        elif value is None:
            inpt.attrs.pop('value', None)
        else:
            inpt['value'] = value
        return self.body


class InputGroup():
    @property
    def prepend(self):
        return self.text('.prepend.input-group-text')

    @prepend.setter
    def prepend(self, val):
        self._set_element(
            val, 
            parent_selector='span.prepend-wrapper',
            target_selector='span.prepend.input-group-text', 
            gen_target=self._gen_input_group_div,
            args=['prepend']
        )

    @property
    def append(self):
        return self.text('.append.input-group-text')
    
    @append.setter
    def append(self, val):
        self._set_element(
            val,
            parent_selector='span.append-wrapper',
            target_selector='span.append.input-group-text',
            gen_target=self._gen_input_group_div,
            args=['append']
        )
    
    def _gen_input_group_div(self, type_):
        """Generate input group prepend/append <div> Tag
        
        `type_` is 'prepend' or 'append'
        """
        input_group_div = Tag(name='div')
        input_group_div['class'] = 'input-group-'+type_
        span = Tag(name='span')
        span['class'] = [type_, 'input-group-text']
        input_group_div.append(span)
        return input_group_div