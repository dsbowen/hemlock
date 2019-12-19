"""Label question polymorph"""

from hemlock.question_polymorphs.utils import *


class Label(HTMLQuestion):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'label'}

    @HTMLQuestion.init('Label')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.soup = render_template('form-group.html', q=self)
        return {'page': page, **kwargs}