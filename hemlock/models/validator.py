"""Validator database model

A Question may contain a list of Validators. A Validator ensure that the
Participant entered a valid answer for the question to which it belongs.

Validators execute a validation function, which takes its Question as its
first argument. The valiation function returns an error message if the
Participant's response was invalid. Otherwise, it returns None.

Validation occurs after post functions are executed.
"""

from hemlock.factory import db
from hemlock.database_types import FunctionType
from hemlock.models.private.base import Base

from sqlalchemy_mutable import MutableListType, MutableDictType


class Validator(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    index = db.Column(db.Integer)
    
    validation = db.Column(FunctionType)
    validation_args = db.Column(MutableListType)
    validation_kwargs = db.Column(MutableDictType)
    
    def __init__(
            self, question=None, index=None, 
            validation=None, validation_args=[], validation_kwargs={}):
        db.session.add(self)
        db.session.flush([self])
        
        self.set_question(question, index)
        self.validation = validation
        self.validation_args = validation_args
        self.validation_kwargs = validation_kwargs
    
    def set_question(self, question, index=None):
        self._set_parent(question, index, 'question', 'validators')
    
    def _validate(self):
        """Validate Participant response
        
        Validation function returns an error message if the Participant's
        response was invalid. Otherwise it returns None.
        """
        return self.validation(
            self.question, *self.validation_args, **self.validation_kwargs)