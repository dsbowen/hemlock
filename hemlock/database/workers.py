"""Worker models"""

from hemlock.app import db
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
        from hemlock.database import Branch, Page
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