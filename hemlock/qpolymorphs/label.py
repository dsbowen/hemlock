"""Label only question"""

from hemlock.qpolymorphs.utils import *

class Label(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'label'}

    @Question.init('Label')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('form-group.html', q=self)
        return {'page': page, **kwargs}