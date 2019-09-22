"""Create experiment as a web application"""

from survey import *
from settings import settings

from hemlock import create_app
from hemlock.app import db, socketio
from hemlock.database.private import DataStore

app = create_app(settings)
if __name__ == '__main__':
    socketio.run(app)
    
@app.shell_context_processor
def make_shell_context():
    db.create_all()
    if not DataStore.query.first():
        DataStore()
    return globals()