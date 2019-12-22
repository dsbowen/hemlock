"""Choice database model
Certain Question polymorphs, such as MultiChoice, contain a list of Choices. 
Each choice specifies:    
1. A text: to be displayed on the page
2. A value: stored as the Question's data by default
3. A label: to identify the Choice when the data are downloaded
"""

from hemlock.app import db
from hemlock.database.private import HTMLBase

from flask import current_app, render_template
from sqlalchemy_mutable import MutableType


class Choice(HTMLBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'choice',
        'polymorphic_on': type
    }
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    index = db.Column(db.Integer)
    _selected_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _selected_index = db.Column(db.Integer)
    _nonselected_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    _nonselected_index = db.Column(db.Integer)
    
    name = db.Column(db.Text)
    value = db.Column(MutableType)
    
    @HTMLBase.init('Choice')
    def __init__(self, question=None, **kwargs):
        super().__init__()
        self.body = render_template('choice.html', c=self)
        self.set_all(kwargs.pop('label', None))
        return {'question': question, **kwargs}
        
    def set_all(self, val):
        self.label = self.name = self.value = val
    
    def is_default(self):
        """Indicate if self is a default choice

        Default is assumed to a be a choice or list of choices.
        """
        default = self.question.response or self.question.default
        if isinstance(default, list):
            return self in default
        return self == default


class Option(Choice):
    id = db.Column(db.Integer, db.ForeignKey('choice.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'option'}

    @HTMLBase.init('Option')
    def __init__(self, question=None, **kwargs):
        super(HTMLBase, self).__init__()
        self.body = render_template('option.html', opt=self)
        self.set_all(kwargs.pop('label', None))
        return {'question': question, **kwargs}

    @property
    def label(self):
        return self.text('option')
    
    @label.setter
    def label(self, val):
        self._set_element((val or ''), parent_selector='option')
        self.body.changed()
    
    def _render(self):
        option_tag = self.body.select_one('option')
        option_tag['name'] = option_tag['value'] = self.question.model_id
        if self.is_default():
            option_tag['selected'] = None
        return self.body