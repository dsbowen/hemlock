"""Select question"""

from hemlock.question_polymorphs.utils import *


class Select(ChoiceQuestion):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args = {'polymorphic_identity': 'select'}

    @HTMLQuestion.init('Select')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.soup = render_template('select_q.html', q=self)
        return {'page': page, **kwargs}

    