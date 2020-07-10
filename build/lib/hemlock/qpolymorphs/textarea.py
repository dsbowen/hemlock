"""# Textarea"""

from ..app import db, settings
from ..models import Question
from .input_group import InputGroup

from flask import render_template

def debug_func(driver, question):
    """
    Default debug function for textarea questions. See
    [`hemlock.functions.debug.random_keys`](debug_functions.md).

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.Textarea
    """
    from ..functions.debug import random_keys
    return random_keys(driver, question)

settings['Textarea'] = {
    'debug_functions': debug_func,
    'rows': 3,
}


class Textarea(InputGroup, Question):
    """
    Textareas provide large text boxes for free responses.

    Inherits from [`hemlock.qpolymorphs.InputGroup`](input_group.md) and 
    [`hemlock.Question`](question.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Textarea label.

    template : str, default='hemlock/textarea.html'
        Template for the textarea body.

    Attributes
    ----------
    rows : int, default=3
        Number of rows of text to display.

    textarea : bs4.Tag
        The `<textarea>` tag.

    Notes
    -----
    Textareas have a default javascript which displays the number of words and
    characters entered. This *cannot* be overridden by passing a `js` argument
    to the constructor, although javascript can be modified after the 
    constructor has finished.

    Examples
    --------
    ```python
    from hemlock import Page, Textarea, push_app_context

    app = push_app_context()

    Page(Textarea('<p>This is a textarea.</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'textarea'}

    def __init__(self, page=None, template='hemlock/textarea.html', **kwargs):
        super().__init__(page, template, **kwargs)
        self.js = render_template('hemlock/textarea.js', self_=self)

    @property
    def rows(self):
        return self.textarea.attrs.get('rows')

    @rows.setter
    def rows(self, val):
        self.textarea['rows'] = val
        self.body.changed()

    @property
    def placeholder(self):
        return self.textarea.get('placeholder')

    @placeholder.setter
    def placeholder(self, val):
        self.textarea['placeholder'] = val
        self.body.changed()

    @property
    def textarea(self):
        return self.body.select_one('textarea#'+self.model_id)

    def textarea_from_driver(self, driver):
        """
        Get textarea from the webdriver for debugging.
        
        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver
            Selenium webdriver (does not need to be `Chrome`).

        Returns
        -------
        textarea : selenium.webdriver.remote.webelement.WebElement
            Web element of the `<textarea>` tag associated with this model.
        """
        return driver.find_element_by_css_selector('textarea#'+self.model_id)

    def _render(self, body=None):
        body = body or self.body.copy()
        textarea = body.select_one('#'+self.model_id)
        textarea.string = self.response or self.default or ''
        return super()._render(body)

    