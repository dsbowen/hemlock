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


class Validator(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    index = db.Column(db.Integer)
    validate = db.Column(FunctionType)
    
    def __init__(self, question=None, index=None, validate=None):
        self.set_question(question, index)
        self.validate = validate
        super().__init__()
    
    def set_question(self, question, index=None):
        self._set_parent(question, index, 'question', 'validators')