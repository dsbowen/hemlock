###############################################################################
# Choice model
# by Dillon Bowen
# last modified 02/12/2019
###############################################################################

from hemlock import db
from hemlock.models.base import Base

'''
Data:
_question_id: ID of the question to which the choice belongs
_order: order in which the choice appears in the question
_text: choice text
_value: encoded value of the choice
_label: choice label, used to record order data
_selected: indicator that this choice was selected
'''
class Choice(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _order = db.Column(db.Integer)
    _text = db.Column(db.Text)
    _value = db.Column(db.PickleType)
    _label = db.Column(db.String(16))
    _selected = db.Column(db.Boolean)
    
    # Add choice to database and commit on initialization
    def __init__(self, question=None, order=None, text='', 
        value=None, label=None, selected=False):
        
        self.assign_question(question, order)
        self.set_text(text)
        self.set_value(value)
        self.set_label(label)
        self.set_selected(selected)
        
        db.session.add(self)
        db.session.commit()
        
    # Assign to question
    def assign_question(self, question, order=None):
        if question is not None:
            self._assign_parent('_question', question, question._choices.all(), order)
        
    # Remove from question
    def remove_question(self):
        if self._question is not None:
            self._remove_parent('_question', self._question._choices.all())
        
    # Set the choice text
    def set_text(self, text):
        self._set_text(text)
        
    # Get the choice text
    def get_text(self):
        return self._text
        
    # Set the encoded value of the choice
    def set_value(self, value=None):
        if value is None:
            self._value = self._text
        else:
            self._value = value
            
    # Set the choice label
    def set_label(self, label=None):
        if label is None:
            self._label = self._text
        else:
            self._label = label
            
    # Set the choice as selected
    def set_selected(self, selected=True):
        self._selected = selected