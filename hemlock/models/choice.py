###############################################################################
# Choice model
# by Dillon Bowen
# last modified 03/19/2019
###############################################################################

from hemlock.factory import db
from hemlock.models.private.base import Base



'''
Relationships:
    question: question to which this choice belongs
    
Columns:
    text: choice text
    value: choice value (same as choice text by default)
    label: choice label (same as choice text by default)
    
    checked: indicator that this choice is a default answer
'''
class Choice(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _index = db.Column(db.Integer)
    
    _text = db.Column(db.Text)
    _value = db.Column(db.PickleType)
    _label = db.Column(db.String(16))
    
    _checked = db.Column(db.String(8))
    
    
    
    # Initialization
    def __init__(
            self, question=None, text='',
            index=None, value=None, label=''):
        
        db.session.add(self)
        db.session.commit()
        
        self.question(question, index)
        self.text(text)
        self.value(value)
        self.label(label)



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
        
    # Remove from question
    def remove_question(self):
        self._remove_parent('_question')
        
        
    # TEXT, VALUE, AND LABEL
    # Set the choice text
    # also resets value and label to new text by default
    def text(self, text='', reset_value=True, reset_label=True):
        self._set_text(text)
        if reset_value:
            self.value(text)
        if reset_label:
            self.label(text)
        
    # Get the choice text
    def get_text(self):
        return self._text
        
    # Set the encoded value of the choice
    def value(self, value=None):
        self._value = value
            
    # Get the encoded value
    def get_value(self):
        return self._value
            
    # Set the choice label
    def label(self, label=''):
        self._label = label
        
    # Get the label
    def get_label(self):
        return self._label
    
    
    
    ###########################################################################
    # Private methods
    ###########################################################################
    
    # Set the choice as checked
    def _set_checked(self, checked=True):
        self._checked = 'checked' if checked else ''