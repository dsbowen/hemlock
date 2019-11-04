"""Download button"""

from hemlock.app import db
from hemlock.database.private import Base
from hemlock.question_polymorphs.imports import *

from flask_download_btn import DownloadBtnManager, DownloadBtnMixin, HandleFormMixin, CreateFileMixin


@DownloadBtnManager.register
class Download(DownloadBtnMixin, Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'download'}

    def __init__(self, page=None, **kwargs):
        DownloadBtnMixin.__init__(self)
        Question.__init__(self, ['download_settings'], page, **kwargs)
        self.js.append(self.script())

    def _render(self):
        content = self.render_btn() + self.render_progress()
        return DIV.format(q=self, content=content)


DIV = """
<div id="{q.model_id}" class="{q._div_classes}">
    {content}
</div>
"""


class HandleForm(HandleFormMixin, Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    btn_id = db.Column(db.Integer, db.ForeignKey('download.id'))


class CreateFile(CreateFileMixin, Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    btn_id = db.Column(db.Integer, db.ForeignKey('download.id'))