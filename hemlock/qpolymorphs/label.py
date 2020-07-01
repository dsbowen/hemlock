"""# Label"""

from ..app import db
from ..models import Question

class Label(Question):
    """
    This question contains a label and does not receive input from the 
    participant.

    Parameters
    ----------
    page : hemlock.Page or None, default=None
        Page to which this label belongs.

    template : str, default='hemlock/form-group.html'
        Path to the Jinja template for the label body.

    Examples
    --------
    ```python
    from hemlock import Page, Label, push_app_context

    push_app_context()

    p = Page()
    Label(p, label='<p>Lorem ipsum.</p>')
    p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'label'}

    def __init__(
            self, page=None, template='hemlock/form-group.html', **kwargs
        ):
        super().__init__(page, template, **kwargs)