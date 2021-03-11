"""# Input"""

from .bases import InputBase
from ..app import db, settings
from ..functions.debug import random_input
from ..models import Question

settings['Input'] = {
    'class': ['form-control'], 'type': 'text', 'debug': random_input
}


class Input(InputBase, Question):
    """
    Inputs take text input by default, or other types of html inputs.

    Inherits from [hemlock.models.InputBase`](bases.md) and 
    [`hemlock.Question`](../models/question.md).

    Parameters
    ----------
    label : str or None, default=None
        Input label.

    template : str, default='hemlock/input.html'
        Template for the input body.
    
    Examples
    --------
    ```python
    from hemlock import Input, Page, push_app_context

    app = push_app_context()

    Page(Input('Input text here.')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'input'}

    def __init__(self, label=None, template='hemlock/input.html', **kwargs):
        super().__init__(label=label, template=template, **kwargs)