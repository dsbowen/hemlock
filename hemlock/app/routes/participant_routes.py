"""Routes for experiment Participants

Workers integrate with the main survey route as follows:
1. Based on the request method, the survey view function returns a get() or 
post() function.
2. If a subroutine of the get() or post() function requires a worker, the
function sends the subroutine to a Redis queue and renders a temporary loading
page.
3. The loading page connects a socket listening on a dedicated namespace for 
the page which called the worker.
4. A worker grabs the subroutine from the Redis queue and executes it. When
finished, the page to which the subroutine belongs stores an indicator that
the job has finished.
5. When the worker finishes executing the subroutine, it emits a 
'job_finished' message on the dedicated namespace.
6. Upon receiving the 'job_finished' message, the socket calls a function to
replace the window location with a new call to the survey route. Because the
page now indicates that the subroutine has finished, it knows not to execute
the subroutine again on the new request.
"""

from hemlock.app.factory import bp, db, socketio
from hemlock.database.models import Participant, Page
from hemlock.question_polymorphs import Text
from hemlock.database.private import DataStore, PageHtml

from datetime import datetime, timedelta
from flask import current_app, flash, jsonify, Markup, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
import rq

"""Initial views and functions"""
@bp.route('/')
def index():
    """Initial view function
    
    Direct visitors to survey, restart page, or screenout page.
    """
    meta = get_metadata()
    if is_screenout(meta):
        return redirect(url_for('hemlock.screenout'))
    
    in_progress = current_user.is_authenticated
    duplicate = is_duplicate(meta)
    if in_progress:
        if duplicate or not current_app.restart_option:
            return redirect(url_for('hemlock.survey'))
        return redirect(url_for('hemlock.restart', **meta))
    if duplicate:
        return redirect(url_for('hemlock.screenout'))

    initialize_participant(meta)
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
        func=time_out, trigger='date', run_date=end_time, 
        args=(current_app._get_current_object(), part.id), id=str(part.id)
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
    """Indicate that this visitor should be screened out
    
    This function compares the metadata of a visitor (visitor) to a dict
    of tracked metadata (tracked). Tracked metadata may be from screenouts 
    or previous study participants. 
    
    Keys specifies the keys on which to look for a match between the visitor 
    metadata and tracked metadata.
    """
    for key in keys:
        visitor_val = visitor.get(key)
        tracked_vals = tracked.get(key)
        if (visitor_val is not None and tracked_vals is not None 
            and visitor_val in tracked_vals):
            return True
    return False

@bp.route('/screenout')
def screenout():
    p = Page(forward=False)
    q = Text(p, text=current_app.screenout_text)
    p.compile()
    return p.render()
    
@bp.route('/restart', methods=['GET','POST'])
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
    p.compile()
    return p.render()

"""Main survey view function"""
@bp.route('/survey', methods=['GET','POST'])
@login_required
def survey():
    """Main survey route

    If time has expired, render the current page with a time expired message. 
    Otherwise, return a function for a GET or POST request. Note that a POST 
    request may be 'in progress' due to callbacks from the Redis queue. In 
    progress POST requests are indicated by page._request_methd.
    """
    return current_user._navigate()

@bp.route('/check_job_status')
def check_job_status():
    """Check the status of a job"""
    job_id = request.args.get('job_id')
    job = rq.job.Job.fetch(job_id, connection=current_app.redis)
    return {'job_finished': job.is_finished}