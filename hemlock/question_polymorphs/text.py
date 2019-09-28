"""Text question polymorph"""

from hemlock.question_polymorphs.imports import *


class Text(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'text'}
    
    def compile_html(self):
        classes = get_classes(self)
        label = get_label(self)
        return QDIV.format(
            id=self.model_id, classes=classes, label=label, content='')
    
    def record_response(self, response):
        return
    
    def record_data(self):
        return