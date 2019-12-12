"""Create web application"""

from survey import *
from settings import settings

from hemlock import create_app
from hemlock.app import db, socketio
from hemlock.database.private import DataStore

import sys

app = create_app(settings)
if __name__ == '__main__':
    socketio.run(app, debug=sys.argv[1]=='True')
    
@app.shell_context_processor
def make_shell_context():
    db.create_all()
    if not DataStore.query.first():
        DataStore()
    return globals()