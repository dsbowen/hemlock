"""# Download button

See <https://dsbowen.github.io/flask-download-btn/> for more details.
"""

from ..app import db
from ..models import Question

from flask import render_template
from flask_download_btn import DownloadBtnManager, DownloadBtnMixin


@DownloadBtnManager.register
class Download(DownloadBtnMixin, Question):
    """
    Allows participants to download files.

    Inherits from 
    [`flask_download_btn.DownloadBtnMixin`](https://dsbowen.github.io/flask-download-btn/download_btn_mixin/) and 
    [`hemlock.Question`](question.md).

    Parameters
    ----------
    label : str or None, default=None
        Download button label.

    template : str, default='hemlock/download.html'
        Download button body template.

    Examples
    --------
    ```python
    from hemlock import Download, Page, push_app_context

    app = push_app_context()

    Page(Download(
    \    '<p>Click here to download a file.</p>',
    \    downloads=('HELLO_WORLD_URL', 'hello_world.txt')
    )).preview()
    ```

    Replace `'HELLO_WORLD_URL'` with your file download URL. Note that the 
    download button will not download your file from a preview.
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'download'}

    def __init__(
            self, label=None, template='hemlock/download.html', **kwargs
        ):
        super().__init__(label=label, template=template, **kwargs)

    def _render_js(self):
        return '\n'.join(self.js + [self.render_script()])