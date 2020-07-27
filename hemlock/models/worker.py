"""# Worker"""

from ..app import db
from .bases import Base

from flask_worker import WorkerMixin

def _set_worker(parent, val, func, worker_attr):
    """
    Set a branch's or page's worker attribute.

    Parameters
    ----------
    parent : hemlock.Branch or hemlock.Page
        The parent to which the worker will be attached.

    val : bool, None, or hemlock.Worker
        The worker to attach to the parent.

    func : callable
        The function for which the worker will be responsible. This is a 
        method of the parent; e.g. `parent._compile`.

    worker_attr : str
        Name of the parent's worker attribute; e.g. `'_compile_worker'`.
    """
    if val:
        worker = val if isinstance(val, Worker) else Worker()
        worker.func = func
    else:
        worker = None
    setattr(parent, worker_attr, worker)


class Worker(WorkerMixin, Base, db.Model):
    """
    Workers simplify interaction with a Redis queue. A worker attaches to a 
    branch or page, and is responsible for one of its methods (compile, 
    validate, submit, or navigate).

    When the method for which a worker is responsible is called, the worker
    sends the method to a Redis queue. While the Redis queue is processing 
    this method, the worker shows participants a loading page. When the Redis
    queue finishes processing this method, the worker sends the client to his
    next page.

    Worker inherits from 
    [`flask_worker.WorkerMixin`](https://dsbowen.github.io.flask-worker/).

    Examples
    --------
    In `survey.py`:

    ```python
    from hemlock import Branch, Compile as C, Label, Page, route

    @route('/survey')
    def start():
    \    return Branch(
    \        Page(
    \            Label('<p>Hello, World!</p>')
    \        ),
    \        Page(
    \            Label(
    \                '<p>Goodbye, Moon!</p>',
    \                compile=C.complex_function(seconds=5)
    \            ),
    \            compile_worker=True,
    \            terminal=True
    \        ),
    \    )

    @C.register
    def complex_function(label, seconds):
    \    import time
    \    for t in range(seconds):
    \        print('Progress: {}%'.format(round(100.*t/seconds)))
    \        time.sleep(1)
    \    print('Progress: 100%')
    ```

    Note that the second page (or rather, one of its questions), needs to run
    a complex compile function. We add a worker to it by setting 
    `compile_worker=True`. Use a similar syntax to add validate, submit, and 
    navigate workers.

    Our `app.py` is standard:

    ```python
    import survey

    from hemlock import create_app

    app = create_app()

    if __name__ == '__main__':
    \    from hemlock.app import socketio
    \    socketio.run(app, debug=True)
    ```

    To run the app locally, you will need to set the `REDIS_URL` environment variable and run a redis queue from your project's root directory.

    **Note.** Windows cannot run redis natively. To run redis on Windows, use [Windows Subsystem for Linux](setup/wsl.md).

    If using the hemlock template and hemlock-CLI:

    1. Add `REDIS_URL: redis://` to `env/local-env.yml`.
    2. Open a second terminal in your project's root directory and enter `hlk rq`.
    3. Run the app by entering `hlk serve` in your first terminal.

    If not using the template or hemlock-CLI:

    1. Set your environment variable with `export REDIS_URL=redis://`.
    2. Open a second terminal in your project's root directory and enter `rq worker hemlock-task-queue`.
    3. Run the app by entering `python3 app.py` in your first terminal.

    Go to <http://localhost:5000/> in your browser. Notice that, when you click past the first page, you see a loading gif before the second page is loaded. In your second terminal window, you should see:

    ```
    Progress: 0%
    ...
    Progress: 100%
    ```

    Instructions for adding redis in production in progress.
    """
    id = db.Column(db.Integer, primary_key=True)
    _compile_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _validate_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _submit_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _navigate_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _navigate_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))