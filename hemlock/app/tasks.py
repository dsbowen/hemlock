from app import app
from hemlock.app.factory import db, socketio

app.app_context().push()

def worker(worker_class, worker_id):
    worker = worker_class.query.get(worker_id)
    if worker is None:
        return
    func = getattr(worker.parent, worker.method_name)
    namespace = '/'+worker.model_id
    return function(func, worker.args, worker.kwargs, namespace)

def model_method(
        model_class, id, method_name, args=[], kwargs={}, namespace=None
        ):
    model = model_class.query.get(id)
    function(getattr(model, method_name), args, kwargs, namespace)

def function(func, args=[], kwargs={}, namespace=None):
    socketio.emit('job_started', namespace=namespace)
    result = func(*args, **kwargs)
    db.session.commit()
    socketio.emit('job_finished', namespace=namespace)
    return result