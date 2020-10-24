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

    Inherits from [`hemlock.InputGroup`](input_group.md) and 
    [`hemlock.ChoiceQuestion`](question.md).

    Its default debug function is
    [`click_choices`](debug_functions.md#hemlockfunctionsdebugclick_choices).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Select question label.

    choices : list of hemlock.Option, str, tuple, or dict, default=[]
        Options which participants can select.

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

    Page(Select('<p>Select one.</p>', ['World','Moon','Star'])).preview()
    ```
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