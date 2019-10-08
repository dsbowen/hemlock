"""Routes for experiment Participants"""

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
@bp.route('/survey/', methods=['GET','POST'])
@login_required
def survey():
    part = current_user
    page = part.current_page
    if part.time_expired:
        flash(current_app.time_expired_text)
        return page.render()
    if request.method == 'POST' or page._request_method == 'POST':
        return post(part, page)
    return get(part, page)
    
def get(part, page):
    """Executed on GET request"""
    if not page._compile_finished:
        if page.compile_worker:
            return page.render_loading(method_name='compile')
        page.compile()
    page._compile_finished = False
    if page.terminal and not part.completed:
        part.update_end_time()
        part.completed = True
    db.session.commit()
    return page.render()

def post(part, page):
    record_response(part, page)
    if page.direction_from == 'back':
        return navigate(part, page)
    return validate(part, page)

def record_response(part, page):
    if not page._response_recorder_finished:
        part.update_end_time()
        part.completed = False
        part.updated = True
        page.record_response()

def validate(part, page):
    if not page._validator_finished:
        if page.validator_worker:
            return page.render_loading(method_name='validate')
        page.validate()
    if page.direction_from == 'invalid':
        return navigate(part, page)
    return submit(part, page)

def submit(part, page):
    if not page._submit_finished:
        if page.submit_worker:
            return page.render_loading(method_name='submit')
        page.submit()
    return navigate(part, page)

def navigate(part, page):
    if page.direction_from == 'back':
        part._back(page.back_to)
    elif page.direction_from == 'forward':
        part._forward(page.forward_to)
    page._request_method = None
    page._response_recorder_finished = False
    page._validator_finished = False
    page._submit_finished = False
    db.session.commit()
    return redirect(url_for('hemlock.survey'))

@bp.route('/check_job_status')
def check_job_status():
    job_id = request.args.get('job_id')
    job = rq.job.Job.fetch(job_id, connection=current_app.redis)
    return {'job_finished': job.is_finished}