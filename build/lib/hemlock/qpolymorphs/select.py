"""# Select (dropdown)"""

from ..app import db, settings
from ..functions.debug import click_choices
from ..models import ChoiceQuestion
from .bases import InputBase
from .choice import OptionListType

from sqlalchemy_mutable import HTMLAttrsType

settings['Select'] = dict(
    input_attrs={'class': ['custom-select'], 'multiple': False},
    debug=click_choices,
)


class Select(InputBase, ChoiceQuestion):
    """
    Select questions allow participants to select one or more options from a 
    dropdown menu.

    Inherits from [`hemlock.InputBase`](bases.md) and 
    [`hemlock.ChoiceQuestion`](../models/question.md).

    Its default debug function is
    [`click_choices`](../functions/debug.md#hemlockfunctionsdebugclick_choices).

    Parameters
    ----------
    label : str or None, default=None
        Select question label.

    choices : list of hemlock.Option, str, tuple, or dict, default=[]
        Options the participant can select.

    template : str, default='hemlock/select.html'
        Template for the select body.

    Attributes
    ----------
    align : str, default='left'
        Choice alignment; `'left'`, `'center'`, or `'right'`.

    choices : list of `hemlock.Option`
        Set for the `choices` parameter.
        
    multiple : bool, default=False
        Indicates that the participant may select multiple choices.

    Examples
    --------
    ```python
    from hemlock import Page, Select, Option, push_app_context

    app = push_app_context()

    Page(
    \    Select(
    \        'Select one.', 
    \        ['World','Moon','Star']
    \    )
    ).preview()
    ```

    Notes
    -----
    An option can be input as any of the following:

    1. `Option` object.
    2. `str`, treated as the choice label.
    3. `(choice label, value)` tuple.
    4. `(choice label, value, name)` tuple.
    5. Dictionary with choice keyword arguments.
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'select'}
    options = db.Column(OptionListType)

    @property
    def choices(self):
        return self.options

    @choices.setter
    def choices(self, val):
        self.options = val

    _input_attr_names = [
        'autofocus',
        'disabled',
        'multiple',
        'required',
        'size'
    ]

    def __init__(
            self, label=None, choices=[], template='hemlock/select.html', 
            **kwargs
        ):
        super().__init__(label, choices, template, **kwargs)