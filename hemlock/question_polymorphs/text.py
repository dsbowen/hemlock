"""Text question polymorph"""

from hemlock.question_polymorphs.imports import *


class Text(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'text'}

    def __init__(self, page=None, **kwargs):
        super().__init__(['text_settings'], page, **kwargs)