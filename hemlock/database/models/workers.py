"""Worker polymorphs"""

from hemlock.app import db
from hemlock.database.private import Base
from hemlock.database.types import MarkupType

from flask import current_app, render_template
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_mutable import MutableListType, MutableDictType


class WorkerMixin(Base):
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def _branch_id(self):
        return db.Column(db.Integer, db.ForeignKey('branch.id'))

    @declared_attr
    def _page_id(self):
        return db.Column(db.Integer, db.ForeignKey('page.id'))

    method_name = db.Column(db.String)
    args = db.Column(MutableListType)
    kwargs = db.Column(MutableDictType)
    css = db.Column(MutableListType)
    js = db.Column(MutableListType)
    template = db.Column(db.String)
    content = db.Column(MarkupType)

    @property
    def parent(self):
        if hasattr(self, 'branch') and self.branch is not None:
            return self.branch
        return self.page

    def __init__(
            self, method_name=None, args=[], kwargs={}, 
            css=None, js=None, template=None, content=None
        ):
        if method_name is not None:
            self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        self.css = css or current_app.worker_css
        self.js = js or current_app.worker_js
        self.js.append(current_app.socket_js)
        self.template = template or current_app.worker_template
        self.content = content or current_app.worker_content
        super().__init__()
    
    def __call__(self):
        db.session.commit()
        job = current_app.task_queue.enqueue(
            'hemlock.app.tasks.worker',
            kwargs={'worker_class': type(self), 'worker_id': self.id}
        )
        html = render_template(self.template, worker=self, job=job)
        return self.render(html)


class CompileWorker(WorkerMixin, db.Model):
    def __init__(self, page=None, *args, **kwargs):
        self.page = page
        self.method_name = 'compile'
        super().__init__(*args, **kwargs)


class ValidatorWorker(WorkerMixin, db.Model):
    def __init__(self, page=None, *args, **kwargs):
        self.page = page
        self.method_name = 'validate'
        super().__init__(*args, **kwargs)


class SubmitWorker(WorkerMixin, db.Model):
    def __init__(self, page=None, *args, **kwargs):
        self.page = page
        self.method_name = 'submit'
        super().__init__(*args, **kwargs)


class NavigatorWorker(WorkerMixin, db.Model):
    def __init__(self, branch=None, page=None, *args, **kwargs):
        self.branch = branch
        self.page = page
        self.method_name = '_grow_branch'
        super().__init__(*args, **kwargs)