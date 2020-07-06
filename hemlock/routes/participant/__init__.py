"""Routes for participants"""

from ...app import bp, db, login_manager, socketio
from ...models import Participant, Page
from ...qpolymorphs import Label
from ...models.private import DataStore

from datetime import datetime, timedelta
from flask import current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

"""Initial views and functions"""
@login_manager.user_loader
def load_user(id):
    return Participant.query.get(id)

@bp.route('/')
def index():
    """
    Direct visitors to survey, restart page, or screenout page.

    Direct to screenout page if:

    1. Visitor metadata is in `app.screenouts`, or
    2. Participant has already completed the survey and is no longer logged in

    Direct to restart page if:

    1. Participant has started the survey and the restart option is available

    Otherwise, direct to default survey route.
    """
    meta = get_metadata()
    if is_screenout(meta):
        return redirect(url_for('hemlock.screenout'))
    
    in_progress = current_user.is_authenticated
    duplicate = is_duplicate(meta)
    if in_progress:
        # DON'T UNDERSTAND THIS LOGIC
        # if duplicate or not current_app.restart_option:
        if not current_app.settings['restart_option']:
            return redirect(url_for('hemlock.'+bp.default_route))
        return redirect(url_for('hemlock.restart', **meta))
    if duplicate:
        return redirect(url_for('hemlock.screenout'))

    initialize_participant(meta)
    return redirect(url_for('hemlock.'+bp.default_route))

def get_metadata():
    """
    This is where it gets meta.

    Returns
    -------
    meta : dict
        Maps URL parameter names to values. This will capture things like
        worker ID for MTurk studies. Additionally, capture IPv4.
    """
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
    part = Participant(meta=meta)
    db.session.commit()
    login_user(part)
    
    # FIX THIS
    # if current_app.time_limit is None:
    #     return
    # end_time = datetime.now() + current_app.time_limit
    # current_app.apscheduler.add_job(
    #     func=time_out, 
    #     trigger='date', 
    #     run_date=end_time, 
    #     args=(current_app._get_current_object(), part.id), 
    #     id=str(part.id)
    # )
        
def time_out(app, part_id):
    """Indicate Participant time has expired"""
    with app.app_context():
        part = Participant.query.get(part_id)
        part.time_expired = True
        db.session.commit()

"""Screenout and duplicate handling"""
def is_screenout(meta):
    """
    Returns
    -------
    match_found : bool
        Indicates that the visitor metadata matched screenouts data.
    """
    return match_found(
        visitor=meta,
        tracked=current_app.screenouts,
        keys=current_app.settings['screenout_keys']
    )

def is_duplicate(meta):
    """
    Returns
    -------
    match_found : bool
        Indicates that the visitor metadata was found in the current survey
        metadata.
    """
    if not current_app.settings['duplicate_keys']:
        return False
    return match_found(
        visitor=meta,
        tracked=DataStore.query.first().meta,
        keys=current_app.settings['duplicate_keys'],
    )

def match_found(visitor, tracked, keys):
    """
    Parameters
    ----------
    visitor : dict
        Visitor metadata.

    tracked : dict
        Tracked metadata from screenouts or current survey metadata.

    keys : iterable
        Keys on which to look for a match.

    Returns
    -------
    match_found : bool
        Indicates that visitor metadata matches tracked metadata on at least
        one key.
    """
    keys = keys or tracked.keys()
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
    p = Page(Label(current_app.settings['screenout_text']), forward=False)
    return p._compile()._render()
    
@bp.route('/restart', methods=['GET','POST'])
@login_required
def restart():
    """
    Participants may navigate back to return to the in progress experiment,
    or forward to restart.
    """
    if request.method == 'POST':
        if request.form.get('direction') == 'forward':
            initialize_participant(get_metadata())
        return redirect(url_for('hemlock.'+bp.default_route))
        
    p = Page(Label(current_app.settings['restart_text']), back=True)
    return p._compile()._render()