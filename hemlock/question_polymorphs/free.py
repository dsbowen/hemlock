"""Free response question"""

from hemlock.question_polymorphs.imports import *


class Free(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'free'}
    
    def _compile(self):
        return super()._compile(content=INPUT.format(q=self))

    @property
    def _default(self):
        return self.response or self.default or ''
    
    def _record_response(self, response):
        self.response = None if response == [''] else response[0]

INPUT = """
<input type="text" class="form-control" id="{q.model_id}" name="{q.model_id}" value="{q._default}">
"""