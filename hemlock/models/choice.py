##############################################################################
# Choice model
# by Dillon Bowen
# last modified 09/07/2019
##############################################################################

from hemlock.factory import attr_settor, db
from hemlock.models.private.base import Base, iscallable
from hemlock.database_types import MutableDict



'''
Relationships:
    question: question to which this choice belongs
    
Columns:
    text: choice text
    value: choice value
    label: choice label
    debug: debug function called by AI Participant
    debug_args: arguments for debug function
    
    _checked: indicator that this choice is a default answer
'''
class Choice(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    index = db.Column(db.Integer)
    
    text = db.Column(db.Text)
    value = db.Column(db.PickleType)
    label = db.Column(db.Text)
    debug = db.Column(db.PickleType)
    debug_args = db.Column(MutableDict)
    
    _checked = db.Column(db.String(8))
    
    
    
    # Initialization
    # by default, value and label are set to text unless manually entered
    def __init__(
            self, question=None, index=None,
            text='', value=None, label=None,
            debug=None, debug_args={}):
        
        db.session.add(self)
        db.session.flush([self])
        
        self.set_question(question, index)
        self.set_all(text)
        if value is not None:
            self.value = value
        if label is not None:
            self.label = label
        self.debug, self.debug_args = debug, debug_args

    # Set question
    def set_question(self, question, index=None):
        self._set_parent(question, index, 'question', 'choices')
        
    # Set text, value, and label
    def set_all(self, text):
        self.text = self.value = self.label = text

    # Set the choice as checked
    def _set_checked(self, checked=True):
        self._checked = 'checked' if checked else ''
        
# Validate function attributes are callable (or None)
@attr_settor.register(Choice, 'debug')
def valid_function(choice, value):
    return iscallable(value)