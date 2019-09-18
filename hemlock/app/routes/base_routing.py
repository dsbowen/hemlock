"""Base routing functions"""

from hemlock.app.factory import bp, db, login_manager
from hemlock.database.models import Participant
from hemlock.database.private import DataStore

from flask import current_app

@login_manager.user_loader
def load_user(id):
    return Participant.query.get(int(id))
    
@bp.before_app_first_request
def init_app():
    """Create database tables and initialize data storage models
    
    Additionally, set a scheduler job to log the status periodically.
    """
    db.create_all()
    if not DataStore.query.first():
        DataStore()
    db.session.commit()
    current_app.apscheduler.add_job(
        func=log_current_status, trigger='interval',
        seconds=current_app.status_log_period.seconds,
        args=[current_app._get_current_object()], id='log_status'
        )

def log_current_status(app):
    with app.app_context():
        ds = DataStore.query.first()
        ds.log_status()
        db.session.commit()