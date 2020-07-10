"""# Worker models

A worker may be attached to a branch or page. Each type of worker is 
responsible for one of its branch's of page's methods, which is expected to 
a be a long-running function. 

When called, the worker sends the method for which it is responsible to a 
Redis queue. While the Redis queue is processing the method, participants 
are shown a loading page. When the worker has finished its job, it returns 
the loaded page to the participant.

All workers inherit from 
[`flask_worker.WorkerMixin`](https://dsbowen.github.io.flask-worker/)..
"""

from ..app import db
from .bases import Base
from .branch import Branch
from .page import Page

from flask_worker import WorkerMixin
from sqlalchemy.ext.declarative import declared_attr


class Worker():
    """
    Convenience methods for adding workers to branches and pages.

    Examples
    --------
    We have two files in our root directory. In `survey.py`:

    ```python
    from hemlock import Branch, Page, Label, Navigate, Worker, route

    @route('/survey')
    def start():
    \    return Worker.navigate(Navigate.end(Branch(
    \        Page(Label('<p>Hello World</p>'))
    \    )))

    @Navigate.register
    def end(origin):
    \    return Branch(Page(Label('<p>Goodbye World</p>'), terminal=True))
    ```

    In `app.py`:

    ```python
    import survey

    from hemlock import create_app

    app = create_app()

    if __name__ == '__main__':
    \    from hemlock.app import socketio
    \    socketio.run(app, debug=True)
    ```

    We'll open two terminal windows. In the first, run:

    ```
    $ rq worker hemlock-task-queue
    ```

    In the second, run:

    ```
    $ python app.py # or python3 app.py
    ```

    Open your browser to <http://localhost:5000>. Click the forward button and
    notice that the Redis queue handles the navigate function.
    """
    def compile(page):
        """
        Parameters
        ----------
        page : hemlock.Page
            Page to which the worker is added.

        Returns
        -------
        page
        """
        page.compile_worker = CompileWorker()
        return page

    def validate(page):
        """
        Parameters
        ----------
        page : hemlock.Page
            Page to which the worker is added.

        Returns
        -------
        page
        """
        page.validate_worker = ValidateWorker()
        return page

    def submit(page):
        """
        Parameters
        ----------
        page : hemlock.Page
            Page to which the worker is added.

        Returns
        -------
        page
        """
        page.submit_worker = SubmitWorker()
        return page

    def navigate(parent):
        """
        Parameters
        ----------
        parent : hemlock.Branch or hemlock.Page
            Branch or page to which the worker is added.

        Returns
        -------
        parent
        """
        parent.navigate_worker = NavigateWorker()
        return parent


class CompileWorker(WorkerMixin, Base, db.Model):
    """
    Handles a page's compile method.

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

    @func.setter
    def func(self, val):
        """Functions are read only"""
        pass


class ValidateWorker(WorkerMixin, Base, db.Model):
    """
    Handles a page's validate method.

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

    @func.setter
    def func(self, val):
        """Functions are read only"""
        pass


class SubmitWorker(WorkerMixin, Base, db.Model):
    """
    Handles a page's submit method.

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

    @func.setter
    def func(self, val):
        """Functions are read only"""
        pass


class NavigateWorker(WorkerMixin, Base, db.Model):
    """
    Handles a branch's or page's navigate method.

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
            return self.branch._navigate
        if self.page:
            return self.page._navigate

    @func.setter
    def func(self, val):
        """Functions are read only"""
        pass

    def __init__(self, parent=None, *args, **kwargs):
        if isinstance(parent, Branch):
            model.branch = parent
        elif isinstance(parent, Page):
            model.page = parent
        super().__init__(*args, **kwargs)