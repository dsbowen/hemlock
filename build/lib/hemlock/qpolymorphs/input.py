"""# Input"""

from ..app import db, settings
from ..functions.debug import send_datetime, send_keys
from ..models import Debug, InputBase, Question
from .input_group import InputGroup

from datetime_selenium import get_datetime

html_datetime_types = (
    'date',
    'datetime-local',
    'month',
    'time',
    'week',
)

@Debug.register
def random_input(driver, question):
    """
    Default debug function for input questions. This function sends a random 
    string or number if the input takes text, or a random `datetime.datetime` 
    object if the input takes dates or times.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.Input
    """
    if question.input_type in html_datetime_types:
        send_datetime(driver, question)
    else:
        send_keys(driver, question)

settings['Input'] = {'input_type': 'text', 'debug': random_input}


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

    placeholder : str or None, default=None
        Html placeholder.

    step : float, str, or None, default=None
        Step attribute for number inputs. By default, the step for number 
        inputs is 1. Set to `'any'` for any step.
    
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

    @property
    def step(self):
        return self.input.get('step')

    @step.setter
    def step(self, val):
        self.input['step'] = val
        self.body.changed()

    def _validate(self, *args, **kwargs):
        return super()._validate(*args, **kwargs)

    def _record_data(self):
        if self.input_type in html_datetime_types:
            self.data = get_datetime(self.response) or None
        elif self.input_type == 'number' and self.response: 
            self.data = (
                float(self.response) if '.' in self.response 
                else int(self.response)
            )
        else:
            super()._record_data()
        return self

    def _submit(self, *args, **kwargs):
        """Convert data to `datetime` object if applicable"""
        return super()._submit(*args, **kwargs)