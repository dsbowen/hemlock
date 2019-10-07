from app import app
from hemlock.app.factory import create_app, db, socketio
from hemlock.database.models import Page

app.app_context().push()

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