"""Base for questions contributing HTML to their pages"""

from hemlock.app import Settings, db
from hemlock.database.question import Question
from hemlock.database.private import HTMLBase

from flask import Markup
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import MutableType

@Settings.register('HTMLQuestion')
def settings():
    return {'css': '', 'js': ''}


class HTMLQuestion(Question, HTMLBase):
    """Function model relationships"""
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

    """Columns"""
    default = db.Column(MutableType)
    response = db.Column(MutableType)

    @Question.init('HTMLQuestion')
    def __init__(self):
        super().__init__()

    """Shortcuts for modifying soup"""
    @property
    def error(self):
        return self.text('.error-txt')

    @error.setter
    def error(self, val):
        form_grp_cls = self.body.select_one('div.form-group')['class']
        if val:
            form_grp_cls.append('error')
        else:
            form_grp_cls.remove('error')
        val = val or ''
        self._set_element(val, 'span.error-txt')
        self.body.changed()

    @property
    def label(self):
        return self.text('.label-txt')

    @label.setter
    def label(self, val):
        val = val or ''
        self._set_element(val, 'span.label-txt')
        self.body.changed()

    """Methods executed during study"""
    def _compile(self):
        [compile_func() for compile_func in self.compile_functions]

    def _render(self):
        return self.soup._render()

    def _record_response(self, response):
        pass
        
    def _validate(self):
        """Validate Participant response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        for validate_func in self.validate_functions:
            self.error = validate_func()
            if self.error is not None:
                return False
        return True

    def _record_data(self):
        self.data = self.response
    
    def _submit(self):
        [submit_func() for submit_func in self.submit_functions]

    def _debug(self, driver):
        [debug_func(driver) for debug_func in self.debug_functions]