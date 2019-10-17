"""Free response question"""

from hemlock.question_polymorphs.imports import *


class Free(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'free'}
    
    def _compile(self):
        default = self.response or self.default or ''
        content = FREE_INPUT.format(id=self.model_id, default=default)
        return super()._compile(content=content)
    
    def _record_response(self, response):
        self.response = None if response == [''] else response[0]

FREE_INPUT = """
<input type="text" class="form-control" id="{id}" name="{id}" value="{default}">
"""