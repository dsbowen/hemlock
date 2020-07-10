"""# Input"""

from ..app import db, settings
from ..models import InputBase, Question
from .input_group import InputGroup

from datetime_selenium import get_datetime

html_datetime_types = (
    'date',
    'datetime-local',
    'month',
    'time',
    'week',
)

def debug_func(driver, question):
    """
    Default debug function for input questions. This function sends a random 
    string or number if the input takes text, or a random `datetime.datetime` 
    object if the input takes dates or times.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.Input
    """
    from ..functions.debug import send_datetime, send_keys
    if question.input_type in html_datetime_types:
        send_datetime(driver, question)
    else:
        send_keys(driver, question)

settings['Input'] = {
    'input_type': 'text',
    'debug_functions': debug_func,
}


class Input(InputGroup, InputBase, Question):
    """
    Inputs take text input by default, or other types of html inputs.

    Inherits from [`hemlock.qpolymorphs.InputGroup`](input_group.md), 
    [`hemlock.models.InputBase`](bases.md) and 
    [`hemlock.Question`](question.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Input label.

    template : str, default='hemlock/input.html'
        Template for the input body.

    Attributes
    ----------
    input_type : str, default='text'
        Type of html input. See <https://www.w3schools.com/html/html_form_input_types.asp>.
    
    Examples
    --------
    ```python
    from hemlock import Input, Page, push_app_context

    app = push_app_context()

    Page(Input('<p>Input text here.</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'input'}

    def __init__(self, label='', template='hemlock/input.html', **kwargs):
        super().__init__(label, template, **kwargs)

    @property
    def input_type(self):
        return self.input.get('type')

    @input_type.setter
    def input_type(self, val):
        self.input['type'] = val
        self.body.changed()

    @property
    def placeholder(self):
        return self.input.get('placeholder')

    @placeholder.setter
    def placeholder(self, val):
        self.input['placeholder'] = val
        self.body.changed()

    def _submit(self, *args, **kwargs):
        """Convert data to `datetime` object if applicable"""
        if self.input_type in html_datetime_types:
            self.data = get_datetime(self.response) or None
        return super()._submit(*args, **kwargs)