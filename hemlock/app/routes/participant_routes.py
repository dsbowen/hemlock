"""Routes for experiment Participants"""

from hemlock.app.factory import bp, db
from hemlock.app.routes.participant_texts import *
from hemlock.database.models import Participant, Page, Question
from hemlock.database.private import DataStore

from datetime import datetime, timedelta
from flask import current_app, flash, Markup, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

"""Initial views and functions"""
@bp.route('/')
@bp.route('/index')
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
        
def render_survey_template(page, question_html):
    return render_template(
        page.survey_template, page=page, question_html=Markup(question_html))

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
    q = Question(p, text=SCREENOUT)
    db.session.delete(p)
    db.session.delete(q)
    return render_survey_template(p, p._compile_question_html())
    
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
    q = Question(p, text=RESTART)
    db.session.delete(p)
    db.session.delete(q)
    return render_survey_template(p, p._compile_question_html())

"""Main survey view function"""
@bp.route('/survey', methods=['GET','POST'])
@login_required
def survey():
    """Main survey route"""
    part = current_user
    page = part.current_page
    
    if part.time_expired:
        flash(TIME_EXPIRED)
        # Do not re-compile question html
        question_html = page.question_html or '' 
    else:
        if request.method == 'POST':
            return post(part, page)
        question_html = page._compile_question_html()

    # PageHtml(page_body)
    
    if page.terminal and not part.completed:
        part.update_end_time()
        part.completed = True
      
    db.session.commit()
    return render_template(
        page.survey_template, page=page, question_html=Markup(question_html))
    
def post(part, page):
    """Function to execute on POST request
    
    1. Update Participant metadata
    2. Navigate in specified direction
    3. Return to survey route with GET request
    """
    part.update_end_time()
    part.completed = False
    part.updated = True
    
    direction = page._submit()        
    if direction == 'forward':
        part._forward(page.forward_to)
    elif direction == 'back':
        part._back(page.back_to)
    part.current_page.direction_to = direction
        
    db.session.commit()
    return redirect(url_for('hemlock.survey'))