"""Validator database model

A Question may contain a list of Validators. A Validator ensure that the
Participant entered a valid answer for the question to which it belongs.

Validators execute a validation function, which takes its Question as its
first argument. The valiation function returns an error message if the
Participant's response was invalid. Otherwise, it returns None.

Validation occurs after response recording and before data recording.
"""

from hemlock.app import db
from hemlock.database.private import Base
from hemlock.database.types import Function, FunctionType


class Validator(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    @property
    def vid(self):
        return 'v{}'.format(self.id)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    index = db.Column(db.Integer)
    validation = db.Column(FunctionType)
    
    def __init__(self, question=None, index=None, validation=Function()):
        db.session.add(self)
        db.session.flush([self])
        self.set_question(question, index)
        self.validation = validation
    
    def set_question(self, question, index=None):
        self._set_parent(question, index, 'question', 'validators')
    
    def validate(self):
        """Validate Participant response
        
        Validation function returns an error message if the Participant's
        response was invalid. Otherwise it returns None.
        """
        return self.validation.call(object=self.question)