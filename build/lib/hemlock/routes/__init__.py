"""View functions"""

from hemlock.app.factory import bp, db
from hemlock.database.private import DataStore
from hemlock.routes.participant import route
import hemlock.routes.participant
import hemlock.routes.researcher

from flask import current_app, session
    
@bp.before_app_first_request
def init_app():
    """Create database tables and initialize data storage models
    
    Additionally, set a scheduler job to log the status periodically.
    """
    session.clear()
    db.create_all()
    if not DataStore.query.first():
        DataStore()
    db.session.commit()
    # FIX THIS
    # current_app.apscheduler.add_job(
    #     func=log_current_status, 
    #     trigger='interval',
    #     seconds=current_app.status_log_period.seconds,
    #     args=[current_app._get_current_object()], 
    #     id='log_status'
    # )

def log_current_status(app):
    """Log participants' status"""
    with app.app_context():
        ds = DataStore.query.first()
        ds.log_status()
        db.session.commit()