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
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash
from datetime import datetime
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
@login_required
def survey():
    part = current_user
    page = part.get_page()
        
    if request.method == 'POST':
        # record page time
        delta = (datetime.utcnow() - part.endtime).total_seconds()
        timer = Question.query.get(page._timer)
        timer.data(timer.get_data()+delta)
        timer._assign_participant(part.id)
        
        navigation = page._validate_on_submit(part.id)
        if navigation != 'invalid' and current_app.record_incomplete:
            part.store_data()
        else:
            part.update_metadata()
        if navigation == 'forward':
            part.forward()
        elif navigation == 'back':
            timer._unassign_participant()
            part.back()
        db.session.commit()
        return redirect(url_for('hemlock.survey'))
        
    rendered_html = page._render_html()
    part.endtime = datetime.utcnow()
    db.session.commit()
    
    if page._terminal:
        [q._assign_participant(part.id) for q in page._questions]
        part.store_data(completed_indicator=True)
        
    return render_template('page.html', page=Markup(rendered_html))

'''
Download data
get data from all participants
write to csv and output
'''
@bp.route('/download', methods=['GET','POST'])
def download():
    x = len(Participant.query.all())
    return 'there are {} participants'.format(x)

    # p = Page()
    # q = Question(p, 'Password', 'free')
    
    # password = ''
    # if request.method == 'POST':
        # password = request.form.get(list(request.form)[0])
    # if not check_password_hash(current_app.password_hash, password):
        # return render_template('page.html', page=Markup(p._render_html()))
    
    ##get main dataframe
    # data = pd.concat([pd.DataFrame(p.get_data()) 
        # for p in Participant.query.all()], sort=False)
    
    write to csv and output
    # resp = make_response(data.to_csv(index_label='index'))
    # resp.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    # resp.headers['Content-Type'] = 'text/csv'
    # return resp
    
# Download list of ipv4 addresses
# for blocking duplicates in subsequent studies
@bp.route('/ipv4', methods=['GET','POST'])
def ipv4():
    p = Page()
    q = Question(p, 'Password', 'free')

    password = ''
    if request.method == 'POST':
        password = request.form.get(list(request.form)[0])
    if not check_password_hash(current_app.password_hash, password):
        return render_template('page.html', page=Markup(p._render_html()))
        
    ipv4 = current_app.ipv4_csv + current_app.ipv4_current
    ipv4 = pd.DataFrame.from_dict({'ipv4':ipv4})
    resp = make_response(ipv4.to_csv(index_label='index'))
    resp.headers['Content-Disposition'] = 'attachment; filename=block.csv'
    resp.headers['Content-Type'] = 'text/csv'
    return resp
    