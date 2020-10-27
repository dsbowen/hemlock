"""# Application setup"""

from ..app import bp, db
from ..models import Participant
from ..models.private import DataStore
from . import participant
from . import researcher

from flask import current_app, session, request
from flask_login import current_user, login_required

from functools import wraps

def route(path, default=False):
    """Decorator for registering a view function

    This decorator wraps a navigate function and converts it into a view 
    function.
    """
    def register_view(gen_root):
        if default or not hasattr(bp, 'default_route'):
            bp.default_route = gen_root.__name__
            
        @bp.route(path, methods=['GET','POST'])
        @login_required
        @wraps(gen_root)
        def view():
            part = get_part()
            if not part.branch_stack:
                part._init_tree(gen_root)
            return part._router()

        return gen_root

    return register_view

def get_part():
    """Get participant

    Normally, a participant is the `current_user` from Flask-Login.

    However, for testing, it is often useful to have multiple surveys open 
    simultaneously. To support this, a participant can also be retrieved by 
    `id` and `_key`. Navigate to {URL}/?Test=1.
    """
    if request.method == 'GET':
        part_id = request.args.get('part_id')
        part_key = request.args.get('part_key')
    else: # request method is POST
        part_id = request.form.get('part_id')
        part_key = request.form.get('part_key')
    if part_id is None:
        part = current_user
    else:
        part = Participant.query.get(part_id)
        assert part_key == part._key
    return part

@bp.before_app_first_request
def init_app():
    """Create database tables and initialize data storage models
    
    Additionally, set a scheduler job to log the status periodically.
    """
    print('before app first request')
    session.clear()
    db.create_all()
    if not DataStore.query.first():
        db.session.add(DataStore())
    db.session.commit()