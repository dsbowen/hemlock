"""Create experiment as a web application"""

from survey import *

from hemlock import create_app
from hemlock.app import db

settings = {
    'start': Start
    }

app = create_app(settings)
    
if __name__ == '__main__':
    app.run()
    
@app.shell_context_processor
def make_shell_context():
    db.create_all()
    return globals()