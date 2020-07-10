"""# Range slider"""

from ..app import db, settings
from ..models import InputBase, Question

from flask import render_template

def debug_func(driver, question):
    """
    Default debug function for range inputs. See 
    [`drag_range`](debug_functions.md).

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.Range
    """
    from ..functions.debug import drag_range
    return drag_range(driver, question)

settings['Range'] = {
    'debug_functions': debug_func,
    'max': 100,
    'min': 0,
    'step': 1,
}


class Range(InputBase, Question):
    """
    Range sliders can be dragged between minimum and maximum values in step 
    increments.

    Inherits from [`hemlock.InputBase`](bases.md) and 
    [`hemlock.Question`](question.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Range label.

    template : str, default='hemlock/range.html'
        Template for the range body.

    Attributes
    ----------
    max : float, default=100
        Maximum value of the range slider.

    min : float, default=0
        Minimum value of the range slider.

    step : float, default=1
        Increments in which the range slider steps.

    Notes
    -----
    Ranges have a default javascript which displays the value of the range 
    slider to participants. This *cannot* be overridden by passing a `js` 
    argument to the constructor, although javascript can be modified after the 
    constructor has finished.

    Examples
    --------
    ```python
    from hemlock import Range, Page, push_app_context

    app = push_app_context()

    Page(Range('<p>This is a range slider.</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'range'}

    def __init__(self, label='', template='hemlock/range.html', **kwargs):
        super().__init__(label, template, **kwargs)
        self.js = render_template('hemlock/range.js', self_=self)

    @property
    def max(self):
        return float(self.input.attrs.get('max', 100))

    @max.setter
    def max(self, val):
        self.input['max'] = val
        self.body.changed()

    @property
    def min(self):
        return float(self.input.attrs.get('min', 0))

    @min.setter
    def min(self, val):
        self.input['min'] = val
        self.body.changed()

    @property
    def step(self):
        return float(self.input.attrs.get('step', 1))

    @step.setter
    def step(self, val):
        self.input['step'] = val
        self.body.changed()