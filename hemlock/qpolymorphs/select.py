"""# Select (dropdown)"""

from ..app import db, settings
from ..models import ChoiceQuestion
from .input_group import InputGroup

def click_choices(driver, question):
    """
    Default select debug function. See [click choices](debug_functions.md).
    """
    from ..functions.debug import click_choices as click_choices_
    click_choices_(driver, question)

settings['Select'] = {
    'align': 'left',
    'inline': False,
    'debug_functions': click_choices,
    'multiple': False,
    'size': None,
}


class Select(InputGroup, ChoiceQuestion):
    """
    Select questions allow participants to select one or more options from a 
    dropdown menu.

    Inherits from [`hemlock.InputGroup`](input_group.md) and 
    [`hemlock.ChoiceQuestion`](question.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Select question label.

    choices : list of str or hemlock.Option, default=[]
        Options which participants can select. String inputs are automatically
        converted to `hemlock.Option` objects.

    template : str, default='hemlock/select.html'
        Template for the select body.

    Attributes
    ----------
    align : str, default='left'
        Choice alignment; `'left'`, `'center'`, or `'right'`.
        
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