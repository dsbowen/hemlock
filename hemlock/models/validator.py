###############################################################################
# Validator model
# by Dillon Bowen
# last modified 02/10/2019
###############################################################################

from hemlock import db
from hemlock.models.base import Base

class Validator(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    condition = db.Column(db.PickleType)
    condition_args = db.Column(db.PickleType)
    order = db.Column(db.Integer)
    
    def __init__(self, question=None, condition=None, args=None, order=None):
        self.assign_question(question, order)
        self.set_condition(condition, args)
        db.session.add(self)
        db.session.commit()
        
    def assign_question(self, question, order=None):
        if question is not None:
            self.assign_parent('question', question, question.validators.all(), order)
        
    def remove_question(self):
        if self.question is not None:
            self.remove_parent('question', self.question.validators.all())
        
    def set_condition(self, condition=None, args=None):
        self.set_function('condition', condition, 'condition_args', args)
        
    # returns error message if response was invalid
    # returns None if response was valid
    def get_error(self):
        return self.call_function(self.question, self.condition, self.condition_args)