"""Choice database model

Question of certain question types, such as multiple choice, contain a list of Choices. Each choice specifies:
    
1. A text: to be displayed on the page
2. A value: stored as the Question's data by default
3. A label: to identify the Choice when the data are downloaded
"""

from hemlock.app import db
from hemlock.database.private import Base
from hemlock.database.types import Function, FunctionType

from sqlalchemy_mutable import MutableType


class Choice(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    index = db.Column(db.Integer)
    _selected_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _selected_index = db.Column(db.Integer)
    _nonselected_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _nonselected_index = db.Column(db.Integer)
    
    text = db.Column(db.Text)
    label = db.Column(db.Text)
    value = db.Column(MutableType)
    debug = db.Column(FunctionType)
    
    def __init__(
            self, question=None, index=None,
            text=None, label=None, value=None, debug=None):
        Base.__init__(self)
        
        self.set_question(question, index)
        self.set_all(text)
        self.value = value if value is not None else self.value
        self.label = label if label is not None else self.label
        self.debug = debug

    def set_question(self, question, index=None):
        self._set_parent(question, index, 'question', 'choices')
        
    def set_all(self, text):
        """Set text, value, and label to the same value"""
        self.text = self.label = self.value = text
    
    def compile_html(self):
        pass