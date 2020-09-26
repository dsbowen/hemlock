from ..app import db
from ..models import ChoiceQuestion


class CheckBase(ChoiceQuestion):
    inline = db.Column(db.Boolean, default=False)

    @property
    def align(self):
        choice_wrapper = self.choice_wrapper
        if not choice_wrapper:
            return
        for class_ in choice_wrapper['class']:
            if class_ == 'text-left':
                return 'left'
            if class_ == 'text-center':
                return 'center'
            if class_ == 'text-right':
                return 'right'

    @align.setter
    def align(self, align_):
        choice_wrapper = self.choice_wrapper
        if not choice_wrapper:
            raise AttributeError('Choice wrapper does not exist')
        align_classes = ['text-'+i for i in ['left','center','right']]
        choice_wrapper['class'] = [
            c for c in choice_wrapper['class'] if c not in align_classes
        ]
        if align_:
            align_ = 'text-' + align_
            choice_wrapper['class'].append(align_)
        self.body.changed()

    @property
    def choice_wrapper(self):
        return self.body.select_one('.choice-wrapper')