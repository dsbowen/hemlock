"""Researcher routes"""

from hemlock.app.factory import bp, db
from hemlock.app.routes.researcher_texts import *
from hemlock.database import Participant, Navbar, Page, Choice, Validate
from hemlock.database.private import DataStore
from hemlock.question_polymorphs import Download, HandleForm, CreateFile, Free, MultiChoice, Text
from hemlock.tools import Static

from flask import Markup, current_app, redirect, request, session, url_for
from functools import wraps
from werkzeug.security import check_password_hash
import os

"""Dashboard Navigation Bar"""
def researcher_navbar():
    return Navbar.query.filter_by(name='researcher_navbar').first()

"""Login"""
@bp.route('/login', methods=['GET','POST'])
def login():
    """Login view function"""
    login_page = get_login_page()
    if request.method == 'POST':
        login_page._record_response()
        password = login_page.questions[0].response
        password = password or ''
        session_store('password', password)
        if login_page._validate():
            return login_successful()
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
    session_store('login_page_id', login_page.id)
    return login_page

def check_password(login_page):
    """Check the input password against researcher password"""
    if not password_correct():
        return PASSWORD_INCORRECT

def password_correct():
    """Indicate that the session password is correct"""
    if 'password' not in session:
        return False
    return check_password_hash(current_app.password_hash, session['password'])

def researcher_login_required(func):
    """Decorator requiring researcher login"""
    @wraps(func)
    def login_requirement():
        if not password_correct():
            get_login_page().error = LOGIN_REQUIRED
            db.session.commit()
            return redirect(url_for('hemlock.login', requested=func.__name__))
        return func()
    return login_requirement

def login_successful():
    """Process successful login

    Clear login page and redirect to requested page.
    """
    login_page = get_login_page()
    login_page.error = None
    login_page.response = None
    db.session.commit()
    requested = request.args.get('requested') or 'participants'
    return redirect(url_for('hemlock.{}'.format(requested)))

def session_store(key, val):
    """Store key, val pair in session

    Remove elements from session until space has cleared.
    """
    session[key] = val
    while key not in session:
        session.pop()
        session[key] = val
    
"""Participant Status"""
@bp.route('/participants')
@researcher_login_required
def participants():
    """View participant's status

    This page displays streamed data on participant status.
    """
    parts_page = get_parts_page()
    parts_page._compile()
    db.session.commit()
    return parts_page._render()

def get_parts_page():
    """Return the Participants dashboard page"""
    if 'parts_page_id' in session:
        return Page.query.get(session['parts_page_id'])
    parts_page = Page(nav=researcher_navbar(), back=False, forward=False)
    parts_page.js.append(current_app.socket_js)
    parts_static = Static(filename='js/participants.js', blueprint='hemlock')
    parts_page.js.append(parts_static)
    q = Text(parts_page)
    q.text = PARTICIPANTS.format(**DataStore.query.first().current_status)
    session_store('parts_page_id', parts_page.id)
    return parts_page
    
"""Download"""
@bp.route('/download')
@researcher_login_required
def download():
    """Download data"""
    download_page = get_download_page()
    download_page._compile()
    db.session.commit()
    return download_page._render()

def get_download_page():
    """Get or create download page"""
    if 'download_page_id' in session:
        return Page.query.get(session['download_page_id'])
    if not os.path.exists('downloads'):
        os.mkdir('downloads')
    download_page = Page(nav=researcher_navbar(), back=False, forward=False)
    files_q = MultiChoice(download_page, text=DOWNLOAD)
    Choice(files_q, text='Metadata', value='meta')
    Choice(files_q, text='Status Log', value='status')
    Choice(files_q, text='Dataframe', value='data')
    btn = Download(download_page, text='Download')
    HandleForm(btn, select_files, args=[files_q])
    session_store('download_page_id', download_page.id)
    return download_page

def select_files(btn, response, files_q):
    """Process download file selection"""
    files_q._record_response(response.getlist(files_q.model_id))
    files_q._record_data()
    data = files_q.data
    btn.filenames.clear()
    btn.create_file_functions.clear()
    if data.get('meta'):
        btn.filenames.append('downloads/Metadata.csv')
        CreateFile(btn, create_meta)
    if data.get('status'):
        btn.filenames.append('downloads/StatusLog.csv')
        CreateFile(btn, create_status)
    if data.get('data'):
        btn.filenames.append('downloads/Data.csv')
        CreateFile(btn, create_data)

def create_meta(btn):
    stage = 'Preparing Metadata'
    yield btn.reset(stage, 0)
    ds = DataStore.query.first()
    ds.meta.save('downloads/Metadata.csv')
    yield btn.report(stage, 100)

def create_status(btn):
    stage = 'Preparing Status Log'
    yield btn.reset(stage, 0)
    ds = DataStore.query.first()
    ds.status_log.save('downloads/StatusLog.csv')
    yield btn.report(stage, 100)

def create_data(btn):
    """
    Some participants will have updated data. Store data from these 
    participants before downloading dataframe.
    """
    stage = 'Storing Participant Data'
    yield btn.reset(stage, 0)
    ds = DataStore.query.first()
    db.session.add(ds)
    updated = Participant.query.filter_by(updated=True).all()
    db.session.add_all(updated)
    for i, part in enumerate(updated):
        yield btn.report(stage, 100.0*i/len(updated))
        ds.store_participant(part)
    ds.data.save('downloads/Data.csv')
    db.session.commit()
    yield btn.report(stage, 100)

"""Logout"""
@bp.route('/logout')
@researcher_login_required
def logout():
    session.clear()
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