"""Base routing functions"""

from hemlock.app.factory import bp, db, login_manager
from hemlock.database.models import Participant, Navbar, Brand, Navitem, Dropdownitem
from hemlock.database.private import DataStore

from flask import current_app, url_for

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
    if not Navbar.query.filter_by(name='researcher_navbar').first():
        create_researcher_navbar()
    db.session.commit()
    current_app.apscheduler.add_job(
        func=log_current_status, trigger='interval',
        seconds=current_app.status_log_period.seconds,
        args=[current_app._get_current_object()], id='log_status'
        )

def create_researcher_navbar():
    navbar = Navbar(name='researcher_navbar')
    Brand(bar=navbar, label='Hemlock')
    Navitem(
        bar=navbar, url=url_for('hemlock.participants'), label='Participants')
    Navitem(bar=navbar, url=url_for('hemlock.download'), label='Download')
    Navitem(bar=navbar, url=url_for('hemlock.logout'), label='Logout')
    return navbar

def log_current_status(app):
    with app.app_context():
        ds = DataStore.query.first()
        ds.log_status()
        db.session.commit()