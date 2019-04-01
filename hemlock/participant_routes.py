###############################################################################
# Participant URL routes for Hemlock survey
# by Dillon Bowen
# last modified 03/28/2019
###############################################################################

# hemlock database, application blueprint, and models
from hemlock.factory import db, bp
from hemlock.models import Participant, Page, Question
from hemlock.models.private import DataStore, Visitors
from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request
from flask_login import login_required, current_user, login_user
from datetime import datetime



###############################################################################
# Initialization functions
###############################################################################

# Initialize database tables upon survey launch
# create a Visitors model to track survey visitors
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
    print('index')
    ipv4 = get_ipv4()
    duplicate_ipv4 = ipv4 in Visitors.query.first().ipv4
    if (ipv4 in current_app.ipv4_csv
        or (current_app.block_dupips and duplicate_ipv4)):
        return redirect(url_for('hemlock.duplicate'))
    Visitors.query.first().append(ipv4)
        
    part = Participant(ipv4, current_app.start)
    return redirect(url_for('hemlock.survey'))
    
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
        
        

###############################################################################
# Survey functions
############################################################################### 
       
# Main survey route
# alternate between GET and POST
    # GET: render current page
    # POST: collect and validate responses, advance to next page
@bp.route('/survey', methods=['GET','POST'])
@login_required
def survey():
    print('survey')
    print('num participants', len(Participant.query.all()))
    if not current_user.is_authenticated:
        return redirect(url_for('hemlock.login'))

    if request.method == 'POST':
        return post()
        
    part = current_user
    page = part._get_current_page()
    compiled_html = page._compile_html()
    if page._terminal:
        part._update_metadata(completed=True)
        DataStore.query.first().store(part)
    db.session.commit()
        
    return render_template('page.html', page=Markup(compiled_html))
    
# Validate and record responses on post request (form submission)
# update metadata
# navigate in the specified direction
# redirect to main survey route
def post():
    part = current_user
    page = part._get_current_page()
    direction = page._validate_on_submit()
    
    part._update_metadata()
        
    if direction == 'forward':
        part._forward(page._forward_to_id)
    elif direction == 'back':
        part._back(page._back_to_id)
        
    db.session.commit()
    return redirect(url_for('hemlock.survey'))