"""Choice database model

Question of certain question types, such as multiple choice, contain a list of Choices. Each choice specifies:
    
1. A text: to be displayed on the page
2. A value: stored as the Question's data by default
3. A label: to identify the Choice when the data are downloaded
"""

from hemlock.app import db
from hemlock.database.private import CompileBase
from hemlock.database.types import Function, FunctionType

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
    debug = db.Column(FunctionType)
    
    def __init__(
            self, question=None, index=None,
            text=None, label=None, value=None, debug=None):
        self.set_question(question, index)
        self.set_all(text)
        self.value = value if value is not None else self.value
        self.label = label if label is not None else self.label
        self.debug = debug
        super().__init__()

    def set_question(self, question, index=None):
        self._set_parent(question, index, 'question', 'choices')
        
    def set_all(self, text):
        """Set text, value, and label to the same value"""
        self.text = self.label = self.value = text
    
    def compile_html(self):
        question=self.question
        classes = ' '.join(question.choice_div_classes)
        checked = 'checked' if self.is_default() else ''
        input = INPUT.format(
            cid=self.model_id, qid=question.model_id,
            type=question.choice_input_type, checked=checked
            )
        text = self.text or ''
        label = LABEL.format(cid=self.model_id, text=text)
        return DIV.format(classes=classes, input=input, label=label)
    
    def is_default(self):
        """Indicate if self is a default choice
        
        Question default is assumed to a be a choice or list of choices.
        """
        default = self.question.response or self.question.default
        if isinstance(default, list):
            return self in default
        return self == default

DIV = """
<div class="{classes}">
    {input}
    {label}      
</div>
"""

INPUT = """
<input id="{cid}" value="{cid}" name="{qid}" class="custom-control-input" type="{type}" {checked}>
"""

LABEL = """
<label class="custom-control-label w-100 choice" for="{cid}">
    {text}
</label>
"""
        