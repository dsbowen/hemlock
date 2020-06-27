"""# Worker models

A worker may be attached to a branch or page. Each type of worker is responsible for one of its branch's of page's methods, which is expected to a be a long-running function. 

When called, the worker sends the method for which it is responsible to a Redis queue. While the Redis queue is processing the method, participants are shown a loading page. When the worker has finished its job, it returns the loaded page to the participant.

All workers inherit from `flask_worker.WorkerMixin`. See <https://dsbowen.github.io.flask-worker/>.
"""

from ..app import db
from .bases import Base
from .branch import Branch
from .page import Page

from flask_worker import WorkerMixin
from sqlalchemy.ext.declarative import declared_attr


class CompileWorker(WorkerMixin, Base, db.Model):
    """
    Handles a page's compile method.

    Parameters
    ----------
    page : hemlock.Page or None, default=None
        The page to which the worker belongs.

    Attributes
    ----------
    func : callable or None
        The page's `_compile` method.

    Relationships
    -------------
    page : hemlock.Page or None
        Set from the `page` parameter.
    """
    id = db.Column(db.Integer, primary_key=True)
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    @property
    def func(self):
        return self.page._compile if self.page else None

    def __init__(self, page=None, *args, **kwargs):
        self.page = page
        super().__init__(*args, **kwargs)


class ValidateWorker(WorkerMixin, Base, db.Model):
    """
    Handles a page's validate method.

    Parameters
    ----------
    page : hemlock.Page or None, default=None
        The page to which the worker belongs.

    Attributes
    ----------
    func : callable or None
        The page's `_validate` method.

    Relationships
    -------------
    page : hemlock.Page or None
        Set from the `page` parameter.
    """
    id = db.Column(db.Integer, primary_key=True)
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    @property
    def func(self):
        return self.page._validate if self.page else None

    def __init__(self, page=None, *args, **kwargs):
        self.page = page
        super().__init__(*args, **kwargs)


class SubmitWorker(WorkerMixin, Base, db.Model):
    """
    Handles a page's submit method.

    Parameters
    ----------
    page : hemlock.Page or None, default=None
        The page to which the worker belongs.

    Attributes
    ----------
    func : callable or None
        The page's `_submit` method.

    Relationships
    -------------
    page : hemlock.Page or None
        Set from the `page` parameter.
    """
    id = db.Column(db.Integer, primary_key=True)
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    
    @property
    def func(self):
        return self.page._submit if self.page else None

    def __init__(self, page=None, *args, **kwargs):
        self.page = page
        super().__init__(*args, **kwargs)


class NavigateWorker(WorkerMixin, Base, db.Model):
    """
    Handles a branch's or page's navigate method.

    Parameters
    ----------
    parent : hemlock.Branch, hemlock.Page, or None, default=None
        The branch or page to which this worker belongs.

    Attributes
    ----------
    func : callable or None
        The branch's or page's `navigate_function`.

    Relationships
    -------------
    branch : hemlock.Branch or None
        Set from the `parent` parameter.

    page : hemlock.Page or None
        Set from the `page` parameter.

    Notes
    -----
    The navigate worker expects to be associated with a branch or page but not 
    both.
    """
    id = db.Column(db.Integer, primary_key=True)
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    
    @property
    def func(self):
        if self.branch:
            return self.branch.navigate_function
        if self.page:
            return self.page.navigate_function

    def __init__(self, parent=None, *args, **kwargs):
        if isinstance(parent, Branch):
            model.branch = parent
        elif isinstance(parent, Page):
            model.page = parent
        super().__init__(*args, **kwargs)