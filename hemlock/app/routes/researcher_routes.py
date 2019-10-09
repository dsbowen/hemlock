"""Researcher routes"""

from hemlock.app.factory import bp, db
from hemlock.app.routes.researcher_texts import *
from hemlock.database import Navbar, Page, Choice, Validate
from hemlock.database.private import DataStore
from hemlock.question_polymorphs import Free, MultiChoice, Text

from flask import Markup, current_app, redirect, request, session, url_for
from functools import wraps
from werkzeug.security import check_password_hash

"""Researcher login"""
@bp.route('/login', methods=['GET','POST'])
def login():
    """Login view function"""
    login_page = get_login_page()
    if request.method == 'POST':
        session['logged_in'] = login_page._validate()
        if session['logged_in']:
            requested = request.args.get('requested') or 'participants'
            return redirect(url_for('hemlock.{}'.format(requested)))
    login_page._compile()
    db.session.commit()
    return login_page._render()

def get_login_page():
    """Get login page

    Create login page if one does not exist already.
    """
    if 'login_page_id' in session:
        return Page.query.get(session['login_page_id'])
    login_page = Page(back=False, forward_button=LOGIN_BUTTON)
    Validate(login_page, check_password)
    Free(login_page, text=PASSWORD_PROMPT)
    session['login_page_id'] = login_page.id
    return login_page

def check_password(login_page):
    """Check the input password against researcher password"""
    q = login_page.questions[0]
    password = '' if q.response is None else q.response
    if not check_password_hash(current_app.password_hash, password):
        return PASSWORD_INCORRECT

def researcher_login_required(func):
    """Decorator requiring researcher login"""
    @wraps(func)
    def login_requirement():
        if 'logged_in' not in session or not session['logged_in']:
            get_login_page().error = LOGIN_REQUIRED
            db.session.commit()
            return redirect(url_for('hemlock.login', requested=func.__name__))
        return func()
    return login_requirement
    
"""Researcher dashboard"""
def researcher_navbar():
    return Navbar.query.filter_by(name='researcher_navbar').first()
    
@bp.route('/participants', methods=['GET','POST'])
@researcher_login_required
def participants():
    """View participant's status

    This page displays streamed data on participant status.
    """
    p = Page(nav=researcher_navbar(), back=False, forward=False)
    p.js.append(current_app.socket_js)
    p.js.append('js/participants.min.js')
    q = Text(p)
    q.text = PARTICIPANTS.format(**DataStore.query.first().current_status)
    return p.compile_html()
    
@bp.route('/download', methods=['GET','POST'])
@researcher_login_required
def download():
    """Download data"""
    p = Page(nav=researcher_navbar(), back=False)
    p.forward_button = DOWNLOAD_BUTTON
    q = MultiChoice(p, text=DOWNLOAD)
    Choice(q, text="Metadata")
    Choice(q, text="Status Log")
    Choice(q, text="Dataframe")
    return p.compile_html()

@bp.route('/logout')
@reseacher_login_required
def logout():
    session['logged_in'] = False
    return redirect(url_for('hemlock.login'))

"""
# hemlock database, application blueprint, and models
from hemlock.factory import viewer, db, bp
from hemlock.models import Participant, Page, Question
from hemlock.models.private import DataStore, Visitors
from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request, flash, jsonify, send_file
from flask_login import login_required, current_user, login_user
from flask_bootstrap import bootstrap_find_resource
from werkzeug.security import check_password_hash
from datetime import datetime
from io import StringIO
import csv




##############################################################################
# Data download views
##############################################################################

# Request data download
@bp.route('/download')
def download():
    if not valid_password():
        return redirect(url_for('hemlock.password', requested_url='download'))
    return render_template(
        'download.html', password=request.args.get('password'))
    
# Get lists of participants with which to update datastore
# to_store_complete: completed participants whose data was not properly stored
# incomplete: incomplete participants
@bp.route('/_get_store_lists')
def _get_store_lists():
    ds = DataStore.query.first()
    participants = Participant.query.all()
    
    to_store_complete = [p for p in participants
        if p.id not in ds.completed_ids and p._metadata['completed']]
    incomplete = [p for p in participants
        if not p._metadata['completed']]
    ds.set_to_store(to_store_complete, incomplete)

    return ''
    
# Update the data store
@bp.route('/_update_data_store')
def _update_data_store():
    return jsonify(finished=DataStore.query.first().update())
        
# Data download
# called after update is finished
@bp.route('/_download')
def _download():
    if not valid_password():
        return redirect(url_for('hemlock.password', requested_url='download'))
    return get_response(data=DataStore.query.first().data, filename='data')



##############################################################################
# ipv4 download view
##############################################################################

# Download list of ipv4 addresses
# for blocking duplicates in subsequent studies
@bp.route('/ipv4', methods=['GET','POST'])
def ipv4():
    if not valid_password():
        return redirect(url_for('hemlock.password', requested_url='ipv4'))
        
    ipv4 = list(set(current_app.ipv4_csv + Visitors.query.first().ipv4))
    return get_response(data={'ipv4': ipv4}, filename='block')



##############################################################################
# Survey download view
##############################################################################
   
# Download png and docx files with survey pages
# requires input valid participant ID
@bp.route('/survey_view', methods=['GET','POST'])
def survey_view():
    if not valid_password():
        return redirect(url_for(
            'hemlock.password', requested_url='survey_view'))
    
    if request.method == 'POST':
        pid = request.form.get(list(request.form)[0])
        # try:
            # part = Participant.query.get(int(pid))
            # assert part is not None
            # return viewer.survey_view(part)
        # except:
            # error = '<p>Participant ID invalid.</p>'
        part = Participant.query.get(int(pid))
        assert part is not None
        return viewer.survey_view(part)
    else:
        error = None
        
    p = Page()
    q = Question(p, '<p>Participant ID</p>', type='free')
    q.error(error)
    return render_template('page.html', page=Markup(p._compile_html()))


    
##############################################################################
# Password validation and get response
##############################################################################

# Check for valid password
def valid_password():
    password = request.args.get('password')
    if password is None:
        return False
    return check_password_hash(current_app.password_hash, password)
    
# Request a password
@bp.route('/password', methods=['GET','POST'])
def password():
    requested_url = 'hemlock.{}'.format(request.args.get('requested_url'))
    if request.method == 'POST':
        password = request.form.get(list(request.form)[0])
        return redirect(url_for(requested_url, password=password))
        
    p = Page()
    Question(p, 'Password', type='free')
    return render_template('page.html', page=Markup(p._compile_html()))
    
# Create response csv from data dictionary in format {'key':[values]}
def get_response(data, filename):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(data.keys())
    cw.writerows(zip(*data.values()))
    
    resp = make_response(si.getvalue())
    disposition = 'attachment; filename={}.csv'.format(filename)
    resp.headers['Content-Disposition'] = disposition
    resp.headers['Content-Type'] = 'text/csv'
    return resp
"""