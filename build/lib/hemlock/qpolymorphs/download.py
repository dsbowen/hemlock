"""# Download button

See <https://dsbowen.github.io/flask-download-btn/> for more details.
"""

from ..app import db
from ..models import Question
from ..models.functions import FunctionRegistrar

from bs4 import BeautifulSoup
from flask import current_app, render_template
from flask_download_btn import DownloadBtnManager, DownloadBtnMixin
from sqlalchemy.ext.orderinglist import ordering_list


@DownloadBtnManager.register
class Download(Question, DownloadBtnMixin):
    """
    Allows participants to download files.

    Inherits from 
    [`flask_download_btn.DownloadBtnMixin`](https://dsbowen.github.io/flask-download-btn/download_btn_mixin/) and 
    [`hemlock.Question`](question.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Download button label.

    template : str, default='hemlock/download.html'
        Download button body template.

    Relationships
    -------------
    create_file_functions : list of hemlock.CreateFile
        Functions for creating files and executing other operations after 
        form handling and before beginning download. More on [file creation]
        (https://dsbowen.github.io/flask-download-btn/create/).

    handle_form_functions : list of hemlock.HandleForm
        Functions for making the download button responsive to web forms. 
        These functions are executed before file creation functions. More on 
        [form handling](https://dsbowen.github.io/flask-download-btn/form/).

    Examples
    --------
    ```python
    from hemlock import Download, Page, push_app_context

    app = push_app_context()

    Page(Download(
    \    '<p>Click here to download a file.</p>',
    \    downloads=[('HELLO_WORLD_URL', 'hello_world.txt')]
    )).preview()
    ```

    Replace `'HELLO_WORLD_URL'` with your file download URL. Note that the 
    download button will not download your file from a preview.
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'download'}

    create_file_functions = db.relationship(
        'CreateFile',
        order_by='CreateFile.index',
        collection_class=ordering_list('index')
    )

    handle_form_functions = db.relationship(
        'HandleForm',
        order_by='HandleForm.index',
        collection_class=ordering_list('index')
    )

    @property
    def body(self):
        return self.btn

    @body.setter
    def body(self, val):
        self.btn = val

    def __init__(self, label='', template='hemlock/download.html', **kwargs):
        db.session.add(self)
        db.session.flush([self])
        if template is not None:
            self.body = render_template(template, self_=self)
        manager = current_app.extensions['download_btn_manager']
        self.progress = render_template(manager.progress_template, btn=self)
        self.downloads = []
        settings = current_app.settings.get('Download')
        settings = settings.copy() if settings else {}
        kwargs['label'] = label
        settings.update(kwargs)
        [setattr(self, key, val) for key, val in settings.items()]

    def _compile(self, *args, **kwargs):
        """Compile

        Begin by compiling the download button javascript. Each time the 
        script is generated, it creates and stores a new CSRF token. 
        Therefore the current script should be replaced by a new script on 
        each compile.
        """
        self.js = self.js or ''
        curr_script = self.js.select_one('#'+self.get_id('script'))
        if curr_script is not None:
            curr_script.extract()
        self.js.append(BeautifulSoup(self.script(), 'html.parser'))
        self.js.changed()
        return super()._compile(*args, **kwargs)

    def _render(self, body=None):
        """Render download button and progress bar"""
        if body is None:
            body = self.body.copy()
            progress = BeautifulSoup(self.render_progress(), 'html.parser')
            body.append(progress)
        return super()._render(body)


class CreateFile(FunctionRegistrar, db.Model):
    """
    Function models for creating files and executing other operations after 
    form handling and before download.

    Inherits from [`hemlock.models.FunctionRegistrar`](functions.md).
    """
    id = db.Column(db.Integer, primary_key=True)
    bnt_id = db.Column(db.Integer, db.ForeignKey('download.id'))


class HandleForm(FunctionRegistrar, db.Model):
    """
    Function models for form handling.

    Inherits from [`hemlock.models.FunctionRegistrar`](functions.md).
    """
    id = db.Column(db.Integer, primary_key=True)
    bnt_id = db.Column(db.Integer, db.ForeignKey('download.id'))