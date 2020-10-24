"""# Textarea"""

from ..app import db, settings
from ..functions.debug import send_keys
from ..models import Question
from .bases import InputBase

from flask import render_template

settings['Textarea'] = {'debug': send_keys, 'class': ['form-control'], 'rows': 3}


class Textarea(InputBase, Question):
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

    Notes
    -----
    Textareas have a default javascript which displays the character and word 
    count to participants. This will be appended to any `js` and `extra_js`
    arguments passed to the constructor.

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

    _input_attr_names = [
        'class',
        'autofocus',
        'cols',
        'disabled',
        'maxlength',
        'placeholder',
        'readonly',
        'required',
        'rows',
        'wrap'
    ]

    def __init__(
            self, label=None, template='hemlock/textarea.html', **kwargs
        ):
        super().__init__(label=label, template=template, **kwargs)
        self.js.append(render_template('hemlock/textarea.js', q=self))