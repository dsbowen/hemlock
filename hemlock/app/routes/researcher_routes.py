"""Researcher routes"""

from hemlock.app.factory import bp, db
from hemlock.app.routes.researcher_texts import *
from hemlock.database import *
from hemlock.database.private import DataStore
from hemlock.question_polymorphs import *
from hemlock.tools import JS

from flask import Markup, current_app, redirect, request, session, url_for
from flask_download_btn import S3File
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
    if request.method == 'GET':
        session.clear()
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
    parts_js = JS(filename='js/participants.js', blueprint='hemlock')
    parts_page.js.append(parts_js)
    parts_q = Text(parts_page)
    Compile(parts_q, update_text)
    session_store('parts_page_id', parts_page.id)
    return parts_page

def update_text(parts_q):
    ds = DataStore.query.first()
    parts_q.text = PARTICIPANTS.format(**ds.current_status)
    
"""Download"""
@bp.route('/download', methods=['GET','POST'])
@researcher_login_required
def download():
    """Download data"""
    download_page = get_download_page()
    download_page._compile()
    rendered = download_page._render()
    db.session.commit()
    return rendered

def get_download_page():
    """Get or create download page"""
    if 'download_page_id' in session:
        return Page.query.get(session['download_page_id'])
    download_page = Page(nav=researcher_navbar(), back=False, forward=False)
    files_q = MultiChoice(download_page, text=SELECT_FILES_TXT)
    Choice(files_q, text='Metadata', value='meta')
    Choice(files_q, text='Status Log', value='status')
    Choice(files_q, text='Dataframe', value='data')
    survey_view_q = Free(download_page, text=SURVEY_VIEW_TXT)
    Validate(survey_view_q, valid_part_ids)
    Submit(survey_view_q, store_part_ids)
    btn = Download(
        download_page, text='Download', callback=request.url,
        download_msg='Download Complete'
    )
    HandleForm(btn, handle_download_form)
    session_store('download_page_id', download_page.id)
    return download_page

def valid_part_ids(survey_view_q):
    part_ids = parse_part_ids(survey_view_q.response)
    invalid_ids = []
    for id in part_ids:
        if Participant.query.get(id) is None:
            invalid_ids.append(id)
    if invalid_ids:
        if len(invalid_ids) == 1:
            return INVALID_ID.format(invalid_ids[0])
        return INVALID_IDS.format(', '.join(invalid_ids))

def store_part_ids(survey_view_q):
    survey_view_q.data = parse_part_ids(survey_view_q.response)

def parse_part_ids(raw_ids):
    if raw_ids is None:
        return []
    comma_splits = raw_ids.split(',')
    space_splits = [cs.split(' ') for cs in comma_splits]
    return [i for ss in space_splits for i in ss if i]

def handle_download_form(btn, response):
    """Process download file selection"""
    download_page = get_download_page()
    db.session.add(download_page)
    btn.downloads = []
    btn.create_file_functions = []
    files_q, survey_view_q, _ = download_page.questions
    download_page._record_response()
    download_page._validate()
    if download_page.is_valid():
        download_page._submit()
        select_files(btn, files_q.data)
        select_survey_view(btn, survey_view_q.data)
    db.session.commit()

def select_files(btn, files):
    s3_file = S3File(
        current_app.s3_client, 
        bucket=os.environ.get('BUCKET')
    )
    if files.get('meta'):
        s3_file.key = 'Metadata.csv'
        btn.downloads.append(s3_file.gen_download())
        CreateFile(btn, create_meta)
    if files.get('status'):
        s3_file.key = 'StatusLog.csv'
        btn.files.append(s3_file.gen_download())
        CreateFile(btn, create_status)
    if files.get('data'):
        s3_file.key = 'Data.csv'
        btn.files.append(s3_file.gen_download())
        CreateFile(btn, create_data)

def create_meta(btn):
    stage = 'Preparing Metadata'
    yield btn.reset(stage, 0)
    ds = DataStore.query.first()
    ds.meta.save('Metadata.csv')
    yield btn.report(stage, 100)

def create_status(btn):
    stage = 'Preparing Status Log'
    yield btn.reset(stage, 0)
    ds = DataStore.query.first()
    ds.status_log.save(os.path.join(btn.tmpdir, 'StatusLog.csv'))
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
    ds.data.save(os.path.join(btn.tmpdir, 'Data.csv'))
    db.session.commit()
    yield btn.report(stage, 100)

def select_survey_view(btn, part_ids):
    if not part_ids:
        return
    CreateFile(btn, create_view, args=part_ids)

def create_view(btn, *part_ids):
    parts = [Participant.query.get(id) for id in part_ids]
    gen = current_app.extensions['viewer'].survey_view(btn, parts)
    for event in gen:
        yield event

"""Logout"""
@bp.route('/logout')
@researcher_login_required
def logout():
    session.clear()
    return redirect(url_for('hemlock.login'))