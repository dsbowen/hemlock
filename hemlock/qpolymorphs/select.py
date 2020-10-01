"""# Select (dropdown)"""

from ..app import db, settings
from ..functions.debug import click_choices
from ..models import ChoiceQuestion, Option
from .input_group import InputGroup

settings['Select'] = {
    'align': 'left',
    'inline': False,
    'debug': click_choices,
    'multiple': False,
    'size': None,
}


class Select(InputGroup, ChoiceQuestion):
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

    select : bs4.Tag
        `<select>` tag.

    size : int or None, default=None
        Number of rows of choices to display.

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
    choice_cls = Option

    def __init__(
            self, label='', choices=[], template='hemlock/select.html', 
            **kwargs
        ):
        super().__init__(label, choices, template, **kwargs)

    @property
    def multiple(self):
        return 'multiple' in self.select.attrs

    @multiple.setter
    def multiple(self, val):
        assert isinstance(val, bool)
        if val:
            self.select['multiple'] = None
        else:
            self.select.attrs.pop('multiple', None)
        self.body.changed()

    @property
    def select(self):
        return self.body.select_one('select#'+self.model_id)

    @property
    def size(self):
        return self.select.attrs.get('size')

    @size.setter
    def size(self, val):
        if not val:
            self.select.attrs.pop('size', None)
        else:
            self.select['size'] = val
        self.body.changed()