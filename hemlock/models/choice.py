###############################################################################
# Choice model
# by Dillon Bowen
# last modified 02/15/2019
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
_checked: indicator that this choice was checked
'''
class Choice(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _order = db.Column(db.Integer)
    _text = db.Column(db.Text)
    _value = db.Column(db.PickleType)
    _value_followstext = db.Column(db.Boolean, default=True)
    _label = db.Column(db.String(16))
    _label_followtext = db.Column(db.Boolean, default=True)
    _checked = db.Column(db.String(8))
    
    # Add choice to database and commit on initialization
    def __init__(self, question=None, text='', value=None, label=None,
        order=None):
        
        db.session.add(self)
        db.session.commit()
        
        self.assign_question(question, order)
        self.text(text)
        self.value(value)
        self.label(label)

    # Assign to question
    def assign_question(self, question, order=None):
        self._assign_parent(question, order)
        
    # Remove from question
    def remove_question(self):
        self._remove_parent('_question')
        
    # Set the choice text
    def text(self, text):
        self._set_text(text)
        
    # Get the choice text
    def get_text(self):
        return self._text
        
    # Set the encoded value of the choice
    def value(self, value=None):
        self._value = value
            
    # Get the encoded value
    def get_value(self):
        if self._value is None:
            return self._text
        return self._value
            
    # Set the choice label
    def label(self, label=None):
        self._label = label
        
    # Get the label
    def get_label(self):
        if self._label is None:
            return self._text
        return self._label
            
    # Set the choice as checked
    def _set_checked(self, checked=True):
        self._checked = 'checked' if checked else ''