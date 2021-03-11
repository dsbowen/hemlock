"""# Application setup"""

from ..app import bp, db
from ..models import Participant
from . import participant
from . import researcher

from flask import current_app, session, redirect, request
from flask_login import current_user, login_required

import os
from functools import wraps

@bp.route('/favicon.ico')
def favicon():
    return redirect('https://dsbowen.github.io/assets/images/hemlock_favicon.png')

@bp.errorhandler(500)
def internal_server_error(e):
    # set in_progress to False to let the router know it should retry when the
    # participant refreshes the page
    current_user._router.in_progress = False
    db.session.commit()
    return current_app.settings['error_500_page'], 500

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