"""Free response question"""

from hemlock.question_polymorphs.imports import *


class Free(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'free'}

    @property
    def _default(self):
        return self.response or self.default or ''

    def __init__(self, page=None, **kwargs):
        super().__init__(['free_settings'], page, **kwargs)
    
    def _render(self):
        return super()._render(content=INPUT.format(q=self))
    
    def _record_response(self, response):
        print(response)
        self.response = None if response == [''] else response[0]

INPUT = """
<input type="text" class="form-control" id="{q.model_id}" name="{q.model_id}" value="{q._default}">
"""