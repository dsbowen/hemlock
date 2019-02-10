###############################################################################
# Choice model
# by Dillon Bowen
# last modified 02/10/2019
###############################################################################

from hemlock import db
from hemlock.models.base import Base

class Choice(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    order = db.Column(db.Integer)
    text = db.Column(db.Text)
    value = db.Column(db.PickleType)
    selected = db.Column(db.Boolean)
    
    def __init__(self, question=None, order=None, text='', value=None, selected=False):
        self.assign_question(question, order)
        self.set_text(text)
        self.set_value(value)
        self.set_selected(selected)
        db.session.add(self)
        db.session.commit()
        
    def set_value(self, value=None):
        if value is None:
            self.value = self.text
        else:
            self.value = value
            
    def set_selected(self, selected=True):
        self.selected = selected
            
    def assign_question(self, question, order=None):
        if question is not None:
            self.assign_parent('question', question, question.choices.all(), order)
        
    def remove_question(self):
        if self.question is not None:
            self.remove_parent('question', self.question.children.all())