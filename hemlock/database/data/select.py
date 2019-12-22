"""Select question"""

from hemlock.question_polymorphs.utils import *

from sqlalchemy.orm import validates


class Select(InputGroup, ChoiceQuestion):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'select'}

    @HTMLQuestion.init('Select')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('select.html', q=self)
        return {'page': page, **kwargs}

    def _render(self):
        option_wrapper = self.body.select_one('span.option-wrapper')
        [option_wrapper.append(c._render()) for c in self.choices]
        return self.body