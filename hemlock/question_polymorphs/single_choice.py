"""Single choice question"""

from hemlock.question_polymorphs.imports import *

from sqlalchemy_mutable import MutableListType


class SingleChoice(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'singlechoice'}
    
    def __init__(self, page=None, **kwargs):
        super().__init__(['single_choice_settings'], page, **kwargs)

    def _render(self):
        content = ''.join([choice._compile() for choice in self.choices])
        return super()._render(content=content)
    
    def _record_response(self, choice_model_id):
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
        self.response = selected
        self.selected_choices = [] if selected is None else [selected]
        self.nonselected_choices = [
            c for c in self.choices if c != selected]
    
    def _record_data(self):
        self.data = None if self.response is None else self.response.value