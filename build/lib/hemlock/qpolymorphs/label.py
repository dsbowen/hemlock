"""# Label"""

from ..app import db, settings
from ..models import Question

settings['Label'] = {'data': 1}

class Label(Question):
    """
    This question contains a label and does not receive input from the 
    participant.

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Question label.

    template : str, default='hemlock/form-group.html'
        Path to the Jinja template for the label body.

    Examples
    --------
    ```python
    from hemlock import Label, Page, push_app_context

    app = push_app_context()

    Page(Label('<p>Hello World</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'label'}

    def __init__(
            self, label='', template='hemlock/form-group.html', **kwargs
        ):
        super().__init__(label, template, **kwargs)

    def _record_data(self):
        return self