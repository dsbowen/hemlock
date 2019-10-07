from app import app
from hemlock.app.factory import create_app, db, socketio
from hemlock.database.models import Page

app.app_context().push()

def task_wrapper(page_id):
    print('wrapping task')
    page = Page.query.get(page_id)
    print('got page', page)
    namespace = '/'+page.model_id
    socketio.emit('job_started', namespace=namespace)
    page.compile()
    page.compiled = True
    db.session.commit()
    socketio.emit('job_finished', namespace=namespace)