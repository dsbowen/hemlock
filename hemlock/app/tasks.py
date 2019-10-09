"""Convenience methods for Redis"""

from app import app
from hemlock.app import db, socketio

app.app_context().push()

def worker(worker_class, worker_id):
    """Run the method specified by a Worker instance

    Begin by recovering the Worker from its class and id. The Worker executes
    a method (specified by method_name) from its parent object. The socket
    notifications associated with this job are emitted on a unique namespace
    given by the worker model id.
    """
    worker = worker_class.query.get(worker_id)
    assert worker is not None, 'Error: Redis could not find Worker.'
    func = getattr(worker.parent, worker.method_name)
    namespace = '/'+worker.model_id
    return function(func, worker.args, worker.kwargs, namespace)

def function(func, args=[], kwargs={}, namespace=None):
    """Execute a function (job)

    Socket emits notifications for the start and end of the job.
    """
    socketio.emit('job_started', namespace=namespace)
    result = func(*args, **kwargs)
    db.session.commit()
    socketio.emit('job_finished', namespace=namespace)
    return result