"""Check question

`Check` questions use radio inputs (if not `multiple`) or checkbox inputs 
(if `multiple`).

By default, choices are positioned vertically. To position them 
horizontally, set `inline` to True.
"""

from hemlock.qpolymorphs.utils import *


class Check(ChoiceQuestion):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'check'}

    multiple = db.Column(db.Boolean, default=False)
    inline = db.Column(db.Boolean, default=False)

    @ChoiceQuestion.init('Check')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('check.html', q=self)
        return {'page': page, **kwargs}
    
    @property
    def center(self):
        return 'text-center' in self._choice_wrapper()['class']

    @center.setter
    def center(self, val):
        """Add the 'text-center' class to the choice wrapper"""
        assert isinstance(val, bool)
        if val == self.center:
            return
        choice_wrapper = self._choice_wrapper()
        if val:
            choice_wrapper['class'].append('text-center')
        else:
            choice_wrapper['class'].remove('text-center')
        self.body.changed()