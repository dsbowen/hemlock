"""# Check"""

from ..app import db, settings
from ..functions.debug import click_choices
from ..models import ChoiceQuestion, ChoiceListType


class CheckBase(ChoiceQuestion):
    """
    Base for `hemlock.Binary` and `hemlock.Check` question types. Inherits 
    from [`hemlock.ChoiceQuestion`](question.md).

    Attributes
    ----------
    align : str, default='left'
        Alignment of the choice text. Value can be `'left'`, `'center'`, 
        or `'right'`.

    inline : bool, default=False
        Indicates that choices should be 
        [inline](https://getbootstrap.com/docs/4.0/components/forms/#inline), 
        as opposed to vertical.
    """
    choices = db.Column(ChoiceListType)
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


settings['Check'] = {
    'align': 'left',
    'inline': False,
    'debug': click_choices,
    'multiple': False,
}


class Check(CheckBase):
    """
    Check questions use radio inputs if only one choice can be selected, or 
    checkbox inputs if multiple choices can be selected.

    Inherits from [`hemlock.qpolymorphs.check.CheckBase`](check.md).

    Its default debug function is 
    [`click_choices`](debug_functions.md#hemlockfunctionsdebugclick_choices).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Check question label.

    choices : list of hemlock.Choice, str, tuple, or dict, default=[]
        Choices which participants can check.

    template : str, default='hemlock/check.html'
        Template for the check body.

    Attributes
    ----------
    choices : list of `hemlock.Choice`
        Set from the `choices` parameter.

    inline : default=False

    multiple : bool, default=False
        Indicates that the participant may select multiple choices.

    Examples
    --------
    ```python
    from hemlock import Check, Page, push_app_context

    app = push_app_context()

    Page(Check('<p>Check one.</p>', ['Yes','No','Maybe'])).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'check'}

    def __init__(
            self, label='', choices=[], template='hemlock/check.html', 
            **kwargs
        ):
        super().__init__(label, choices, template, **kwargs)


settings['Binary'] = {
    'align': 'left',
    'inline': True,
    'debug': click_choices,
    'multiple': False,
    'record_choice_index': False,
}


class Binary(CheckBase):
    """
    Binary question use radio inputs and have two options, coded as 0 and 1.

    Inherits from [`hemlock.qpolymorphs.check.CheckBase`](check.md).

    Its default debug function is 
    [`click_choices`](debug_functions.md#hemlockfunctionsdebugclick_choices).
    
    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Check question label.

    choices : list of [str, str], default=['Yes', 'No']
        Choices which participants can check. The first choice is coded as 1,
        the second as 0.

    template : str, default='hemlock/check.html'
        Template for the check body.

    Attributes
    ----------
    choices : list of `hemlock.Choice`
        Set from the `choices` parameter.
        
    inline : bool, default=True

    multiple : bool, default=False
        Indicates that the participant may select multiple choices.

    Examples
    --------
    ```python
    from hemlock import Binary, Page, push_app_context

    app = push_app_context()

    Page(Binary('<p>Yes or no?</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'binary'}

    def __init__(
            self, label='', choices=['Yes', 'No'], 
            template='hemlock/check.html', **kwargs
        ):
        assert len(choices) == 2, 'Binary question require 2 choices'
        choices = [(choices[0], 1), (choices[1], 0)]
        super().__init__(label, choices, template, **kwargs)