###############################################################################
# Participant URL routes for Hemlock survey
# by Dillon Bowen
# last modified 03/11/2019
###############################################################################

# hemlock database, application blueprint, and models
from hemlock.factory import db, bp
from hemlock.models import Participant, Page, Question

# flask functions
from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request
from flask_login import login_required, current_user, login_user

# other tools
from datetime import datetime

# Create database tables upon survey launch
@bp.before_app_first_request
def before_first_app_request():
    db.create_all()
    
    

# Participant initialization
@bp.route('/')
def index():
    # record ipv4 and exclude as specified
    ipv4 = get_ipv4()
    if (ipv4 in current_app.ipv4_csv
        or (current_app.block_dupips and ipv4 in current_app.ipv4_current)):
        return redirect(url_for('hemlock.duplicate'))
    current_app.ipv4_current.append(ipv4)
        
    # register new participant and begin survey
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
        <p>Thank you for your continuing interest in our research.</p>
        ''')
    return render_template('page.html', page=Markup(page._compile_html()))
        
        
        
# Main survey route
# alternate between GET and POST
    # GET: render current page
    # POST: collect and validate responses, advance to next page
@bp.route('/survey', methods=['GET','POST'])
@login_required
def survey():
    # validate and record responses on post request
    if request.method == 'POST':
        return post()
        
    # get current user and page
    part = current_user
    page = part.get_page()
        
    # compile page html
    compiled_html = page._compile_html()
    
    # update participant end time
    part.endtime = datetime.utcnow()
    
    db.session.commit()
    
    # store data on terminal page
    if page._terminal:
        [q._assign_participant(part.id) for q in page._questions]
        part.store_data(completed_indicator=True)
        
    return render_template('page.html', page=Markup(compiled_html))
    
# Validate and record responses on post request (form submission)
def post():
    part = current_user
    page = part.get_page()
    
    # get direction from (forward, back, invalid)
    direction = page._validate_on_submit(part.id)
    
    # record incomplete data, or update metadata (end time and completed)
    if direction != 'invalid' and current_app.record_incomplete:
        part.store_data()
    else:
        part.update_metadata()
        
    # navigate in the specified direction
    if direction == 'forward':
        part.forward()
    elif direction == 'back':
        part.back()
        
    db.session.commit()
    return redirect(url_for('hemlock.survey'))