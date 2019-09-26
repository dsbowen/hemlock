"""Create experiment as a web application"""

from survey import *
from settings import settings

from hemlock import create_app
from hemlock.app import db, socketio
from hemlock.database.private import DataStore
from hemlock.app.routes.base_routing import create_researcher_navbar

app = create_app(settings)
if __name__ == '__main__':
    socketio.run(app)
    
@app.shell_context_processor
def make_shell_context():
    db.create_all()
    if not DataStore.query.first():
        DataStore()
    if not Navbar.query.first():
        create_researcher_navbar()
    return globals()