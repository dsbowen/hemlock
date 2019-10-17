"""Choice database model

Certain Question polymorphs, such as MultiChoice, contain a list of Choices. 

Each choice specifies:    
1. A text: to be displayed on the page
2. A value: stored as the Question's data by default
3. A label: to identify the Choice when the data are downloaded
"""

from hemlock.app import db
from hemlock.database.private import CompileBase

from sqlalchemy_mutable import MutableType


class Choice(CompileBase, db.Model):
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
    
    def __init__(
            self, question=None, index=None,
            text=None, label=None, value=None
        ):
        self.set_question(question, index)
        self.set_all(text)
        self.value = value if value is not None else self.value
        self.label = label if label is not None else self.label
        super().__init__()

    def set_question(self, question, index=None):
        self._set_parent(question, index, 'question', 'choices')
        
    def set_all(self, text):
        """Set text, value, and label to the same value"""
        self.text = self.label = self.value = text
    
    def is_default(self):
        """Indicate if self is a default choice

        Default is assumed to a be a choice or list of choices.
        """
        default = self.question.response or self.question.default
        if isinstance(default, list):
            return self in default
        return self == default

    def _compile(self):
        return DIV.format(c=self, q=self.question)

    @property
    def _div_classes(self):
        return ' '.join(self.question.choice_div_classes)

    @property
    def _checked(self):
        return 'checked' if self.is_default() else ''

    @property
    def _text(self):
        return self.text if self.text is not None else ''

DIV = """
<div class="{c._div_classes}">
    <input id="{c.model_id}" value="{c.model_id}" name="{q.model_id}" class="custom-control-input" type="{q.choice_input_type}" {c._checked}>
    <label class="custom-control-label w-100 choice" for="{c.model_id}">
        {c._text}
    </label>     
</div>
"""     