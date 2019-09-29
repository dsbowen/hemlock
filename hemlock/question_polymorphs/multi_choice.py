"""Multiple choice question"""

from hemlock.question_polymorphs.imports import *

CHOICE_DIV_CLASSES = ['custom-control', 'custom-checkbox']
INPUT_TYPE = 'checkbox'


class MultiChoice(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'multichoice'}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.choice_div_classes:
            self.choice_div_classes = CHOICE_DIV_CLASSES
        if self.choice_input_type is None:
            self.choice_input_type = INPUT_TYPE
    
    def compile_html(self):
        content = ''.join([choice.compile_html() for choice in self.choices])
        return super().compile_html(content=content)
    
    def record_response(self, choice_model_ids):
        selected, nonselected = [], []
        for choice in self.choices:
            if choice.model_id in choice_model_ids:
                selected.append(choice)
            else:
                nonselected.append(choice)
        self.response = selected.copy()
        self.default = selected.copy()
        self.selected_choices = selected.copy()
        self.nonselected_choices = nonselected
    
    def record_data(self):
        """Record data using one-hot encoding"""
        self.data = {c.value: int(c in self.response) for c in self.choices}
    
    def pack_data(self):
        var = self.var
        if self.data is None:
            return {var+choice.value: None for choice in self.choices}
        packed_data = {var+key: self.data[key] for key in self.data.keys()}
        return super().pack_data(packed_data)