"""Download button"""

from hemlock.qpolymorphs.utils import *

from bs4 import BeautifulSoup
from flask_download_btn import DownloadBtnManager, DownloadBtnMixin, CreateFileMixin, HandleFormMixin


@DownloadBtnManager.register
class Download(DownloadBtnMixin, InputGroup, InputBase, Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'download'}

    @property
    def body(self):
        return self.btn

    @body.setter
    def body(self, val):
        self.btn = val

    @Question.init('Download')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('download.html', q=self)
        return {'page': page, **kwargs}

    def _compile(self, *args, **kwargs):
        """Compile

        Begin by compiling the download button javascript. Each time the script is generated, it creates and stores a new CSRF token. Therefore the current script should be replaced by a new script on each compile.
        """
        curr_script = self.js.select_one('#'+self.model_id)
        if curr_script is not None:
            curr_script.extract()
        new_script = BeautifulSoup(self.script(), 'html.parser')
        self.js.append(new_script)
        self.js.changed()
        super()._compile(*args, **kwargs)

    def _render(self, body=None):
        if body is None:
            body = self.body.copy()
            progress = BeautifulSoup(self.render_progress(), 'html.parser')
            body.append(progress)
        return super()._render(body)


class CreateFile(CreateFileMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bnt_id = db.Column(db.Integer, db.ForeignKey('download.id'))

class HandleForm(HandleFormMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bnt_id = db.Column(db.Integer, db.ForeignKey('download.id'))