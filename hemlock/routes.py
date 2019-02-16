###############################################################################
# URL routes for Hemlock survey
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

from hemlock import db, bp
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable
from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request
import io
import csv
import pandas as pd

# Create database tables upon survey launch
@bp.before_app_first_request
def before_first_app_request():
    db.create_all()

# Create participant and root branch before beginning survey
# (option) exlcude if duplicate ipv4 from csv or current study
@bp.route('/')
def index():
    ipv4 = get_ipv4()
    if (ipv4 in current_app.ipv4_csv
        or (current_app.block_dupips and ipv4 in current_app.ipv4_current)):
        return redirect(url_for('hemlock.duplicate'))
    current_app.ipv4_current.append(ipv4)
        
    part = Participant(ipv4, current_app.start)
    session['part_id'] = part.id
    db.session.commit()
    
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
    page = Page(terminal=True)
    q = Question(page=page, text='''
        <p>Our records indicate that you have already participated in this or similar studies.</p>
        <p>Thank you for your continuing interest in our research.</p>
        ''')
    return render_template('page.html', page=Markup(page._render_html()))
        
'''
Main survey route
alternate between GET and POST
    GET: render current page
    POST: collect and validate responses, advance to next page
store participant data on terminal page
'''
@bp.route('/survey', methods=['GET','POST'])
def survey():
    part = Participant.query.get(session['part_id'])
    page = part.get_page()
        
    if request.method == 'POST':
        navigation = page._validate_on_submit(part.id)
        if navigation == 'forward':
            part.forward()
        elif navigation == 'back':
            part.back()
        else:
            page._set_direction('invalid')
        db.session.commit()
        return redirect(url_for('hemlock.survey'))
        
    if page._terminal:
        page._render_html() # might change this when I record partial responses
        # ASSIGN QUESTIONS TO PART HERE
        # PARTICIPANTS MAY GO BACK AND FORTH FROM THE TERMINAL PAGE, RECORDS DATA MULTIPLE TIMES
        part.store_data()
        
    return render_template('page.html', page=Markup(page._render_html()))
    
'''
Download data
get data from all participants
write to csv and output
'''
@bp.route('/download')
def download():     
    # get main dataframe
    data = pd.concat([pd.DataFrame(p.data) for p in Participant.query.all()],
        sort=False)
        
    # drop unnecessary order variables
    drop_prefix = ['id_','ipv4_', 'start_time_']
    columns = [pref+'{0}order'.format(pv) 
        for pref in drop_prefix for pv in ['p','v']]
    data = data.drop(columns=columns)
    
    # write to csv and output
    resp = make_response(data.to_csv(index_label='index'))
    resp.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    resp.headers['Content-Type'] = 'text/csv'
    return resp
    
# Download list of ipv4 addresses
# for blocking duplicates in subsequent studies
@bp.route('/ipv4')
def ipv4():
    ipv4 = current_app.ipv4_csv = current_app.ipv4_current
    ipv4 = pd.DataFrame.from_dict({'ipv4':ipv4})
    resp = make_response(ipv4.to_csv())
    resp.headers['Content-Disposition'] = 'attachment; filename=block.csv'
    resp.headers['Content-Type'] = 'text/csv'
    return resp
    