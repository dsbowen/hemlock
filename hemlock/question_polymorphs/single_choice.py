"""Single choice question"""

from hemlock.question_polymorphs.imports import *

from sqlalchemy_mutable import MutableListType

CHOICE_DIV_CLASSES = ['custom-control', 'custom-radio']
INPUT_TYPE = 'radio'


class SingleChoice(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'singlechoice'}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.choice_div_classes:
            self.choice_div_classes = CHOICE_DIV_CLASSES
        if self.choice_input_type is None:
            self.choice_input_type = INPUT_TYPE
    
    def compile_html(self):
        content = ''.join([choice.compile_html() for choice in self.choices])
        return super().compile_html(content=content)
    
    def record_response(self, choice_model_id):
        """Record response
        
        Response is a choice model id or None.
        1. Set question response to the value of the selected choice
        2. Set the default choice to the selected choice
        3. Update selected and nonselected choices
        """
        if choice_model_id:
            choice_model_id = choice_model_id[0]
            for choice in self.choices:
                if choice.model_id == choice_model_id:
                    selected = choice
                    break
        else:
            selected = None    
        self.response = self.default = selected
        self.selected_choices = [] if selected is None else [selected]
        self.nonselected_choices = [
            c for c in self.choices if c != selected]
    
    def record_data(self):
        self.data = None if self.response is None else self.response.value