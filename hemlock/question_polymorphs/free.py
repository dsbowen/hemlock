"""Free response question"""

from hemlock.question_polymorphs.imports import *


class Free(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'free'}

    prepend = db.Column(db.Text)
    placeholder = db.Column(db.Text)
    append = db.Column(db.Text)

    @property
    def _prepend(self):
        if self.prepend is None:
            return ''
        return PREPEND.format(q=self)

    @property
    def _placeholder(self):
        return self.placeholder or ''

    @property
    def _default(self):
        return self.response or self.default or ''

    @property
    def _append(self):
        if self.append is None:
            return ''
        return APPEND.format(q=self)

    def __init__(self, page=None, **kwargs):
        super().__init__(['free_settings'], page, **kwargs)
    
    def _render(self):
        return super()._render(content=INPUT_GROUP.format(q=self))
    
    def _record_response(self, response):
        self.response = None if response == [''] else response[0]


INPUT_GROUP = """
<div class="input-group mb-3">
    {q._prepend}
    <input type="text" class="form-control" id="{q.model_id}" name="{q.model_id}" placeholder="{q._placeholder}" value="{q._default}">
    {q._append}
</div>
"""

PREPEND = """
<div class="input-group-prepend">
    <span class="input-group-text">{q.prepend}</span>
</div>
"""

APPEND = """
<div class="input-group-append">
    <span class="input-group-text">{q.append}</span>
</div>
"""