###############################################################################
# Validator model
# by Dillon Bowen
# last modified 02/12/2019
###############################################################################

from hemlock import db
from hemlock.models.base import Base

'''
Data:
_question_id: ID of the question to which the validator belongs
_order: order in which validation appears in question
_condition_function: function which validates participant's response
_condition_args: arguments for the condition function
'''
class Validator(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _order = db.Column(db.Integer)
    _condition_function = db.Column(db.PickleType)
    _condition_args = db.Column(db.PickleType)
    
    # Add to database and commit on initialize
    def __init__(self, question=None, order=None, condition=None, args=None):
        self.assign_question(question, order)
        self.set_condition(condition, args)
        
        db.session.add(self)
        db.session.commit()
        
    # Assign to question
    def assign_question(self, question, order=None):
        if question is not None:
            self._assign_parent('_question', question, question._validators.all(), order)
        
    # Remove from question
    def remove_question(self):
        if self._question is not None:
            self._remove_parent('_question', self._question._validators.all())
        
    # Set the condition function and arguments
    def set_condition(self, condition=None, args=None):
        self._set_function('_condition_function', condition, '_condition_args', args)
        
    # Return error message if response is invalid
    # return None if response was valid
    def _get_error(self):
        return self._call_function(
            self._question, self._condition_function, self._condition_args)