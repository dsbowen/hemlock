"""Choice database model

Question of certain question types, such as multiple choice, contain a list of Choices. Each choice specifies:
    
1. A text: to be displayed on the page
2. A value: stored as the Question's data by default
3. A label: to identify the Choice when the data are downloaded

Choices also have a debugging function and arguments.
"""

from hemlock.factory import db
from hemlock.database_types import FunctionType
from hemlock.models.private import Base

from sqlalchemy_mutable import MutableType, MutableListType, MutableDictType


class Choice(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    index = db.Column(db.Integer)
    _selected_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _selected_index = db.Column(db.Integer)
    _nonselected_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _nonselected_index = db.Column(db.Integer)
    
    text = db.Column(db.Text)
    value = db.Column(db.PickleType)
    label = db.Column(db.Text)
    
    debug = db.Column(FunctionType)
    debug_args = db.Column(MutableListType)
    debug_kwargs = db.Column(MutableDictType)
    
    def __init__(
            self, question=None, index=None,
            text='', value=None, label=None,
            debug=None, debug_args=[], debug_kwargs={}):
        
        db.session.add(self)
        db.session.flush([self])
        
        self.set_question(question, index)
        self.set_all(text)
        self.value = value if value is not None else self.value
        self.label = label if label is not None else self.label
        self.debug = debug
        self.debug_args = debug_args
        self.debug_kwargs = debug_kwargs

    def set_question(self, question, index=None):
        self._set_parent(question, index, 'question', 'choices')
        
    def set_all(self, text):
        """Set text, value, and label to the same value"""
        self.text = self.value = self.label = text