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
        self.question(question, order)
        self.condition(condition, args)
        
        db.session.add(self)
        db.session.commit()
        
    # Assign to question
    def question(self, question, order=None):
        self._assign_parent(question, order)
        
    # Remove from question
    def remove_question(self):
        self._remove_parent('_question')
        
    # Set the condition function and arguments
    def condition(self, condition=None, args=None):
        self._set_function('_condition_function', condition, '_condition_args', args)
        
    # Return error message if response is invalid
    # return None if response was valid
    def _get_error(self):
        return self._call_function(
            self._question, self._condition_function, self._condition_args)
            
    # Copies selected attributes from another validator
    # def _copy(self, validator_id):
        # v = Validator.query.get(validator_id)
        
        # self._set_order(v._order)
        # self.condition(v._condition_function, v._condition_args)