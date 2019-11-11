"""Multiple choice question"""

from hemlock.question_polymorphs.imports import *


class MultiChoice(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'multichoice'}
    
    def __init__(self, page=None, **kwargs):
        super().__init__(['multi_choice_settings'], page, **kwargs)
    
    def _render(self):
        content = ''.join([choice._compile() for choice in self.choices])
        return super()._render(content=content)
    
    def _record_response(self, choice_model_ids):
        selected, nonselected = [], []
        for choice in self.choices:
            if choice.model_id in choice_model_ids:
                selected.append(choice)
            else:
                nonselected.append(choice)
        self.response = selected.copy()
        self.selected_choices = selected.copy()
        self.nonselected_choices = nonselected
    
    def _record_data(self):
        """Record data using one-hot encoding"""
        if self.response is None:
            self.data = None
            return
        self.data = {
            c.value: int(c in self.response) 
            for c in self.choices if c.value is not None
        }
    
    def _pack_data(self):
        var = self.var
        if var is None:
            return super()._pack_data()
        if self.data is None:
            packed_data = {
                var+c.value: None for c in self.choices if c.value is not None
            }
        else:
            packed_data = {var+key: val for key, val in self.data.items()}
        return super()._pack_data(packed_data)