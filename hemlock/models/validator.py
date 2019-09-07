##############################################################################
# Validator model
# by Dillon Bowen
# last modified 09/07/2019
##############################################################################

from hemlock.factory import attr_settor, db
from hemlock.models.private.base import Base, iscallable
from hemlock.database_types import MutableDict



'''
Relationships:
    question: question to which this validator belongs
    
Columns:
    condition: function which determines the validity of response
        Return None if valid, error message if invalid
    condition_args: arguments for condition function
'''
class Validator(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    index = db.Column(db.Integer)
    
    condition = db.Column(db.PickleType)
    condition_args = db.Column(MutableDict)
    
    
    
    # Initialization
    def __init__(
            self, question=None, index=None, 
            condition=None, condition_args=None):
        db.session.add(self)
        db.session.flush([self])
        
        self.set_question(question, index)
        self.condition, self.condition_args = condition, condition_args
    
    # Set question
    def set_question(self, question, index=None):
        self._set_parent(question, index, 'question', 'validators')
    
    # Return error message if response is invalid
    # return None if response was valid
    def _get_error(self):
        return self._call_function(
            self.condition, self.condition_args, self.question)

# Validate function attributes are callable (or None)
@attr_settor.register(Validator, 'condition')
def valid_function(validator, value):
    return iscallable(value)