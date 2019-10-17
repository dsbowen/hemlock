"""Worker models"""

from hemlock.app import db

from flask_worker import WorkerMixin as WorkerBaseMixin


class WorkerMixin(WorkerBaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    @property
    def employer(self):
        return self.page

    def __init__(self, page=None, *args, **kwargs):
        self.page = page
        super().__init__(*args, **kwargs)


class CompileWorker(WorkerMixin, db.Model):
    method_name = '_compile'


class ValidateWorker(WorkerMixin, db.Model):
    method_name = '_validate'


class SubmitWorker(WorkerMixin, db.Model):
    method_name = '_submit'


class NavigateWorker(WorkerMixin, db.Model):
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    method_name = '_navigate'

    @property
    def employer(self):
        return self.branch if self.branch is not None else self.page

    def __init__(self, branch=None, *args, **kwargs):
        self.branch = branch
        super().__init__(*args, **kwargs)