"""# Binary choice"""

from .check_base import CheckBase
from ..app import db, settings
from ..functions.debug import click_choices
from ..models import Choice

settings['Binary'] = {
    'align': 'left',
    'inline': True,
    'debug': click_choices,
    'multiple': False,
}


class Binary(CheckBase):
    """
    Binary question use radio inputs and have two options, coded as 0 and 1.

    Inherits from [`hemlock.ChoiceQuestion`](question.md).

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
    align : str, default='left'
        Choice alignment; `'left'`, `'center'`, or `'right'`.

    choice_wrapper : bs4.Tag
        Tag fo the choice html wrapper.

    inline : bool, default=False
        Indicates that choices should be [inline](https://getbootstrap.com/docs/4.0/components/forms/#inline), 
        as opposed to vertical.

    multiple : bool, default=False
        Indicates that the participant may select multiple choices.

    Examples
    --------
    ```python
    from hemlock import Binary, Page, push_app_context

    app = push_app_context()

    Page(Binary('<p>Yes or no?</p>')).preview()
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