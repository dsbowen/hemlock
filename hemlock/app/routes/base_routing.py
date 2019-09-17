"""Base routing functions"""

from hemlock.app.factory import bp, db, login_manager
from hemlock.database.models import Participant
from hemlock.database.private import DataStore, Metadata, StatusLogger

from flask import current_app

@login_manager.user_loader
def load_user(id):
    return Participant.query.get(int(id))
    
@bp.before_app_first_request
def before_app_first_request():
    """Create database tables and initialize data storage models
    
    Additionally, set a scheduler job to log the status periodically.
    """
    db.create_all()
    if not Metadata.query.first():
        Metadata()
    if not StatusLogger.query.first():
        StatusLogger()
    if not DataStore.query.all():
        DataStore()
    db.session.commit()
    current_app.apscheduler.add_job(
        func=log_current_status, trigger='interval',
        seconds=current_app.status_logger_period.seconds,
        args=[current_app._get_current_object()], id='log_status'
        )

def log_current_status(app):
    with app.app_context():
        logger = StatusLogger.query.first()
        logger.update_log()
        db.session.commit()