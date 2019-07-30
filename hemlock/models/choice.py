##############################################################################
# Choice model
# by Dillon Bowen
# last modified 07/30/2019
##############################################################################

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
    
    debug_function: debug function called by AI Participant
    debug_args: arguments for debug function
    debug_attrs: attributes for Debug Choice
'''
class Choice(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _index = db.Column(db.Integer)
    
    _text = db.Column(db.Text)
    _value = db.Column(db.PickleType)
    _label = db.Column(db.Text)
    
    _checked = db.Column(db.String(8))
    
    _debug_function = db.Column(db.PickleType)
    _debug_args = db.Column(db.PickleType)
    _debug_attrs = db.Column(db.PickleType)
    
    
    
    # Initialization
    # by default, value and label are set to text unless manually entered
    def __init__(
            self, question=None, text='',
            index=None, value=None, label=None,
            debug=None, debug_args=None, debug_attrs=None):
        
        db.session.add(self)
        db.session.commit()
        
        self.question(question, index)
        self.text(text)
        if value is not None:
            self.value(value)
        if label is not None:
            self.label(label)
        self.debug(debug, debug_args, debug_attrs)



    ##########################################################################
    # Public methods
    ##########################################################################
    
    # QUESTION
    # Assign to question
    def question(self, question, index=None):
        self._assign_parent(question, '_question', index)
        
    # Get question
    def get_question(self):
        return self._question
        
    # Get index (position within question)
    def get_index(self):
        return self._index
        
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
        label = label.replace(' ', '_')
        self._label = label
        
    # Get the label
    def get_label(self):
        return self._label
    
    
    # DEBUG FUNCTION AND ARGUMENTS
    # Set the debug function and arguments
    def debug(self, debug=None, args=None, attrs=None):
        self._set_function(
            '_debug_function', debug, 
            '_debug_args', args, 
            '_debug_attrs', attrs)
    
    # Get the debug function
    def get_debug(self):
        return self._debug_function
    
    # Get the debug function arguments
    def get_debug_args(self):
        return self._debug_args
    
    # Get the Debug Page attributes
    def get_debug_attrs(self):
        return self._debug_attrs
    
    
    
    ##########################################################################
    # Private methods
    ##########################################################################
    
    # Set the choice as checked
    def _set_checked(self, checked=True):
        self._checked = 'checked' if checked else ''