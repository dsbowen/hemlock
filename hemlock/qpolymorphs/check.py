"""# Check"""

from .check_base import CheckBase
from ..app import db, settings
from ..functions.debug import click_choices

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

    Inherits from [`hemlock.ChoiceQuestion`](question.md).

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
    align : str, default='left'
        Choice alignment; `'left'`, `'center'`, or `'right'`.

    choices : list of `hemlock.Choice`
        Set from the `choices` parameter.

    choice_wrapper : bs4.Tag
        Tag of the choice html wrapper.

    inline : bool, default=False
        Indicates that choices should be 
        [inline](https://getbootstrap.com/docs/4.0/components/forms/#inline), 
        as opposed to vertical.

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