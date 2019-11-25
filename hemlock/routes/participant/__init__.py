"""Routes for participants

This file is responsible for the participant's initial view code s, as well 
as screenout and duplicate handling. On a request to the index route, it 
determines whether participants are screened out, redirected to the restart 
page, or redirected to the main survey route. 

The main survey route is handled by the participant's router. 
See hemlock/database/private/routing.py
"""

from hemlock.app.factory import bp, db, login_manager, socketio
from hemlock.database import Participant, Page
from hemlock.question_polymorphs import Text
from hemlock.database.private import DataStore

from datetime import datetime, timedelta
from flask import current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

"""Initial views and functions"""
@login_manager.user_loader
def load_user(id):
    return Participant.query.get(int(id))

@bp.route('/')
def index():
    """Initial view function
    
    Direct visitors to survey, restart page, or screenout page.
    """
    print('index')
    meta = get_metadata()
    print('got metadata')
    if is_screenout(meta):
        return redirect(url_for('hemlock.screenout'))
    
    print('checking if user is in progress or duplicate')
    in_progress = current_user.is_authenticated
    duplicate = is_duplicate(meta)
    if in_progress:
        if duplicate or not current_app.restart_option:
            return redirect(url_for('hemlock.survey'))
        return redirect(url_for('hemlock.restart', **meta))
    if duplicate:
        return redirect(url_for('hemlock.screenout'))

    print('init participant')
    initialize_participant(meta)
    print('redirecting')
    return redirect(url_for('hemlock.survey'))

def get_metadata():
    """Get Participant metadata from URL parameters"""
    meta = dict(request.args)
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', None)
    meta['IPv4'] = request.remote_addr if ip is None else ip.split(',')[0]
    return meta

def initialize_participant(meta):
    """Initialize Participant with given metadata
    
    If there is a time limit, start the clock.
    """
    if current_user.is_authenticated:
        logout_user()
    part = Participant(start_navigation=current_app.start, meta=meta)
    db.session.commit()
    login_user(part)
    
    if current_app.time_limit is None:
        return
    end_time = datetime.now() + current_app.time_limit
    current_app.apscheduler.add_job(
        func=time_out, 
        trigger='date', 
        run_date=end_time, 
        args=(current_app._get_current_object(), part.id), 
        id=str(part.id)
    )
        
def time_out(app, part_id):
    """Indicate Participant time has expired"""
    with app.app_context():
        part = Participant.query.get(part_id)
        part.time_expired = True
        db.session.commit()

"""Screenout and duplicate handling"""
def is_screenout(meta):
    """Look for a match between visitor metadata and screenouts"""
    tracked_meta = current_app.screenouts
    keys = current_app.screenout_keys
    return match_found(visitor=meta, tracked=tracked_meta, keys=keys)

def is_duplicate(meta):
    """Look for a match between visitor metadata and previous participants"""
    tracked_meta = DataStore.query.first().meta
    keys = current_app.duplicate_keys
    return match_found(visitor=meta, tracked=tracked_meta, keys=keys)

def match_found(visitor, tracked, keys):
    """Indicate visitor metadata matches tracked metadata on one or more keys
    
    This function compares the metadata of a visitor (visitor) to a dict
    of tracked metadata (tracked). Tracked metadata may be from screenouts 
    or previous study participants.
    
    Keys specifies the keys on which to look for a match between the visitor 
    metadata and tracked metadata.
    """
    for key in keys:
        visitor_val = visitor.get(key)
        tracked_vals = tracked.get(key)
        if (
            visitor_val is not None and tracked_vals is not None 
            and visitor_val in tracked_vals
        ):
            return True
    return False

@bp.route('/screenout')
def screenout():
    p = Page(forward=False)
    q = Text(p, text=current_app.screenout_text)
    p._compile()
    return p._render()
    
@bp.route('/restart', methods=['GET','POST'])
@login_required
def restart():
    """Restart option
    
    Participants may navigate back to return to the in progress experiment,
    or forward to restart.
    """
    if request.method == 'POST':
        if request.form.get('direction') == 'back':
            return redirect(url_for('hemlock.survey'))
        initialize_participant(get_metadata())
        return redirect(url_for('hemlock.survey'))
        
    p = Page(back=True)
    q = Text(p, text=current_app.restart_text)
    p._compile()
    return p._render()

"""Main survey view function"""
@bp.route('/survey', methods=['GET','POST'])
@login_required
def survey():
    return current_user._router.route()