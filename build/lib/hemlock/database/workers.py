"""Worker models

`Worker`s may be attached to `Page` and `Branch` models. A `CompileWorker` 
handles a `Page`'s `Compile` function, a `ValidateWorker` the `Validate` 
function, etc..

`Worker`s send their `employer`'s job to a Redis Queue. While the job is 
enqueued or being processed, the worker sends the participant a loading 
page.

More detail at dsbowen.github.io/flask-worker.
"""

from hemlock.app import Settings, db
from hemlock.database import Branch, Page
from hemlock.database.bases import Base

from flask_worker import WorkerMixin as WorkerBaseMixin
from sqlalchemy.ext.declarative import declared_attr


class WorkerMixin(WorkerBaseMixin, Base):
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def _page_id(self):
        return db.Column(db.Integer, db.ForeignKey('page.id'))

    @property
    def employer(self):
        return self.page

    @employer.setter
    def employer(self, value):
        self.page = value

    @Base.init('Worker')
    def __init__(self, employer=None, *args, **kwargs):
        self.employer = employer
        super().__init__(*args, **kwargs)


class CompileWorker(WorkerMixin, db.Model):
    method_name = '_compile'


class ValidateWorker(WorkerMixin, db.Model):
    method_name = '_validate'


class SubmitWorker(WorkerMixin, db.Model):
    method_name = '_submit'


class NavigateWorker(WorkerMixin, db.Model):
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    method_name = 'navigate_function'

    @property
    def employer(self):
        return self.branch if self.branch is not None else self.page

    @employer.setter
    def employer(self, value):
        if isinstance(value, Branch):
            self.page = None
            self.branch = value
        elif isinstance(value, Page):
            self.branch = None
            self.page = value
        elif value is None:
            self.branch = self.page = None
        else:
            raise ValueError('Employer must be a Branch or Page')