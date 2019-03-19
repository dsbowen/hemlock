###############################################################################
# Validator model
# by Dillon Bowen
# last modified 03/19/2019
###############################################################################

from hemlock.factory import db
from hemlock.models.private.base import Base



'''
Relationships:
    question: question to which this valiator belongs
    
Columns:
    condition_function: function which determines the validity of participant's
        response. Returns None if valid, error message if invalid
    condition_args: arguments for condition function
'''
class Validator(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _index = db.Column(db.Integer)
    
    _condition_function = db.Column(db.PickleType)
    _condition_args = db.Column(db.PickleType)
    
    
    
    # Initialization
    def __init__(self, question=None, condition=None, args=None, index=None):
        db.session.add(self)
        db.session.commit()
        
        self.question(question, index)
        self.condition(condition, args)
    
    
    
    ###########################################################################
    # Public methods
    ###########################################################################
    
    # QUESTION
    # Assign to question
    def question(self, question, index=None):
        self._assign_parent(question, '_question', index)
        
    # Get question
    def get_question(self):
        return self._question
        
    # Get index
    def get_index(self):
        return self._index
        
    # Remove from question
    def remove_question(self):
        self._remove_parent('_question')
    
    
    # CONDITION FUNCTION AND ARGUMENTS
    # Set the condition function and arguments
    def condition(self, condition=None, args=None):
        self._set_function(
            '_condition_function', condition, 
            '_condition_args', args)
            
    # Get condition function
    def get_condition(self):
        return self._condition_function
        
    # Get condition arguments
    def get_condition_args(self):
        return self._condition_args
    
    
    
    ###########################################################################
    # Private methods
    ###########################################################################
    
    # Return error message if response is invalid
    # return None if response was valid
    def _get_error(self):
        return self._call_function(
            self._question, self._condition_function, self._condition_args)