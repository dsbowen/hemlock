"""# Check"""

from ..app import db, settings
from ..functions.debug import click_choices
from ..models import ChoiceQuestion
from .bases import InputBase
from .choice import ChoiceListType

def binary(label=None, choices=['Yes', 'No'], inline=True, **kwargs):
    """
    Creates a binary (yes/no) check question.

    Parameters
    ----------
    label : str, default=None

    choices : list, default=['Yes', 'No']
        List of choice labels.

    inline : bool, default=True
        Indicates that choices should be displayed inline.

    \*\*kwargs :
        Keyword arguments passed to `Check` constructor.

    Examples
    --------
    ```python
    from hemlock import Page, binary, push_app_context

    app = push_app_context()

    Page(binary('Yes or no?')).preview()
    ```
    """
    assert len(choices) == 2, 'Binary question requires exactly 2 choices'
    return Check(
        label, [(choices[0], 1), (choices[1], 0)], inline=inline, **kwargs
    )

def Binary(*args, **kwargs):
    print('WARNING: Deprecation notice. Please use `binary` for future releases')
    return binary(*args, **kwargs)

settings['Check'] = {
    'inline': False,
    'debug': click_choices,
    'multiple': False,
}


class Check(InputBase, ChoiceQuestion):
    """
    Check questions use radio inputs if only one choice can be selected, or 
    checkbox inputs if multiple choices can be selected.

    Inherits from [`hemlock.qpolymorphs.base.InputBase`](bases.md) and [`hemlock.models.ChoiceQuestion`](../models/question.md).

    Its default debug function is 
    [`click_choices`](../functions/debug.md#hemlockfunctionsdebugclick_choices).

    Parameters
    ----------
    label : str or None, default=None
        Check question label.

    choices : list of hemlock.Choice, str, tuple, or dict, default=[]
        Choices which participants can check.

    template : str, default='hemlock/check.html'
        File name of the Jinja template.

    Attributes
    ----------
    align : str, default='left'
        Alignment of the choice text. Value can be `'left'`, `'center'`, 
        or `'right'`.

    choices : list of `hemlock.Choice`
        Set from the `choices` parameter.

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

    Page(Check('Check one.', ['Yes','No','Maybe'])).preview()
    ```

    Notes
    -----
    A choice can be input as any of the following:

    1. `Choice` object.
    2. `str`, treated as the choice label, value, and name.
    3. `(choice label, value)` tuple.
    4. `(choice label, value, name)` tuple.
    5. Dictionary with choice keyword arguments.
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'check'}

    choices = db.Column(ChoiceListType)
    inline = db.Column(db.Boolean, default=False)
    multiple = db.Column(db.Boolean, default=False)

    def __init__(
            self, label=None, choices=[], template='hemlock/check.html', 
            **kwargs
        ):
        super().__init__(label, choices, template, **kwargs)