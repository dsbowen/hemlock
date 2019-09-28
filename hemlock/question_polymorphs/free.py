"""Free response question"""

from hemlock.question_polymorphs.imports import *


class Free(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'free'}
    
    def compile_html(self):
        classes = get_classes(self)
        label = get_label(self)
        default = self.default or ''
        content = FREE_INPUT.format(id=self.model_id, default=default)
        return QDIV.format(
            id=self.model_id, classes=classes, label=label, content=content)
    
    def record_response(self, response):
        response = None if not response else response[0]
        self.response = self.default = response