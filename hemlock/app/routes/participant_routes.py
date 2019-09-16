"""Routes for experiment Participants

# Main survey route
# alternate between GET and POST
# GET: 
    # compile current page and store as PageHtml
    # update metadata and store if page is terminal
    # return rendered page
# POST: collect and validate responses, advance to next page
"""

from hemlock.app.factory import db, bp, login_manager
from hemlock.app.routes.participant_texts import *
from hemlock.database.models import Participant, Page, Question

from datetime import datetime, timedelta
from flask import current_app, flash, Markup, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user

"""Initial views and functions"""
@bp.before_app_first_request
def before_app_first_request():
    db.create_all()
    '''
    if not Visitors.query.all():
        Visitors()
    if not DataStore.query.all():
        DataStore()
    '''
    
@login_manager.user_loader
def load_user(id):
    return Participant.query.get(int(id))
    
@bp.route('/')
@bp.route('/index')
def index():
    """Initial view function"""
    '''
    if current_user.is_authenticated:
        if current_app.block_duplicate_ips:
            return redirect(url_for('hemlock.survey'))
        return redirect(url_for('hemlock.restart'))
    '''
    if current_user.is_authenticated:
        return redirect(url_for('hemlock.survey'))
    meta = get_metadata()
    '''
    duplicate_ipv4 = ipv4 in Visitors.query.first().ipv4
    if (ipv4 in current_app.ipv4_csv
        or (current_app.block_dupips and duplicate_ipv4)):
        return redirect(url_for('hemlock.duplicate'))
    Visitors.query.first().append(ipv4)
    '''
    initialize_participant(meta)
    return redirect(url_for('hemlock.survey'))

def get_metadata():
    """Get IPv4 and other Participant metdata from URL parameters"""
    meta = {}
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', None)
    meta['IPv4'] = request.remote_addr if ip is None else ip.split(',')[0]
    meta.update(request.args)
    return meta

def initialize_participant(meta):
    """Initialize Participant with given metadata
    
    If there is a time limit, start the clock.
    """
    part = Participant(current_app.start, meta)
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
    """Time out the Participant for inactivity"""
    with app.app_context():
        print('time expired')
        part = Participant.query.get(part_id)
        part.time_expired = True
        ### STORE DATA HERE
        db.session.commit()

"""
##############################################################################
# Initialization functions
##############################################################################

# Initialize database tables upon survey launch
# create a Visitors model to track survey visitors
# create two DataStore models
    # DataStore 1 stores data from all participants (incomplete and complete)
    # DataStore 2 stores data only from participants who completed the survey
@bp.before_app_first_request
def before_first_app_request():
    db.create_all()
    
    if not Visitors.query.all():
        Visitors()
    if not DataStore.query.all():
        DataStore()

# Participant initialization
# record ipv4 and exclude as specified
# register new participant and begin survey
@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        if current_app.block_dupips:
            return redirect(url_for('hemlock.survey'))
        return redirect(url_for('hemlock.restart'))
        
    ipv4 = get_ipv4()
    duplicate_ipv4 = ipv4 in Visitors.query.first().ipv4
    if (ipv4 in current_app.ipv4_csv
        or (current_app.block_dupips and duplicate_ipv4)):
        return redirect(url_for('hemlock.duplicate'))
    Visitors.query.first().append(ipv4)
        
    part = Participant(ipv4, current_app.start)
    return redirect(url_for('hemlock.survey'))
    
# Ask participant if they wish to restart the survey
@bp.route('/restart', methods=['GET','POST'])
def restart():
    if request.method == 'POST':
        if request.form.get('direction') == 'back':
            return redirect(url_for('hemlock.survey'))
        logout_user()
        return redirect(url_for('hemlock.index'))
        
    p = Page(back=True)
    q = Question(p, '''
    <p>Click << to return to your in progress survey. Click >> to restart the survey.</p>
    <p>If you choose to restart the survey, your responses will not be saved.</p>''')
    return render_template('page.html', page=Markup(p._compile_html()))
    
# Get user ipv4
def get_ipv4():
    ipv4 = request.environ.get('HTTP_X_FORWARDED_FOR', None)
    if ipv4 is None:
        return request.remote_addr
    return ipv4.split(',')[0]
        
# Exclude message
@bp.route('/duplicate')
def duplicate():
    p = Page(terminal=True)
    q = Question(page=p, text='''
    <p>Our records indicate that you have already participated in this or similar studies.</p>
    <p>Thank you for your continuing interest in our research.</p>''')
    return render_template('page.html', page=Markup(p._compile_html()))
"""  

@bp.route('/survey', methods=['GET','POST'])
@login_required
def survey():
    """Main survey route"""
    part = current_user
    page = part.current_page
    
    if part.time_expired:
        flash(TIME_EXPIRED)
        question_html = page.question_html or ''
    else:
        if request.method == 'POST':
            return post(part, page)
        question_html = page._compile_question_html()

    # PageHtml(page_body)
    
    if page.terminal and not part.completed:
        part.update_end_time()
        part.completed = True
        # DataStore.query.first().store(part)
      
    db.session.commit()
    return render_template(
        page.survey_template, page=page, question_html=Markup(question_html))
    
def post(part, page):
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