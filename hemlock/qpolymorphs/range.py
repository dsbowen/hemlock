"""# Range slider"""

from ..app import db, settings
from ..functions.debug import drag_range
from ..models import Question
from .bases import InputBase

from flask import render_template

settings['Range'] = {
    'debug': drag_range,
    'type': 'range', 
    'class': ['custom-range'], 
    'min': 0, 'max': 100, 'step': 1
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

    Notes
    -----
    Ranges have a default javascript which displays the value of the range 
    slider to participants. This will be appended to any `js` and `extra_js`
    arguments passed to the constructor.

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

    def __init__(self, label=None, template='hemlock/range.html', **kwargs):
        super().__init__(label=label, template=template, **kwargs)
        self.js.append(render_template('hemlock/range.js', q=self))