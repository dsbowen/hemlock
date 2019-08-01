##############################################################################
# Researcher URL routes for Hemlock survey
# by Dillon Bowen
# last modified 08/01/2019
##############################################################################

# hemlock database, application blueprint, and models
from hemlock.factory import db, bp
from hemlock.models import Participant, Page, Question
from hemlock.models.private import DataStore, Visitors
from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request, flash, jsonify, send_file
from flask_login import login_required, current_user, login_user
from flask_bootstrap import bootstrap_find_resource
from werkzeug.security import check_password_hash
from datetime import datetime
from io import StringIO
from docx import Document
from docx.shared import Inches
import csv
import imgkit
import os
import zipfile

SURVEY_VIEW_IMG_WIDTH = Inches(6)




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
   
# Download survey view for a specified participant
@bp.route('/survey_view', methods=['GET','POST'])
def survey_view():
    if not valid_password():
        return redirect(url_for(
            'hemlock.password', requested_url='survey_view'))
    
    if request.method == 'POST':
        return _survey_view()

    p = Page()
    Question(p, 'Participant ID', qtype='free')
    return render_template('page.html', page=Markup(p._compile_html()))
    
# Download survey view (private)
# get requested participant
# render compiled html and add to docx and zip files
# add docx to zip and return zip file
def _survey_view():
    part = _get_participant()
    if part is None:
        return redirect(url_for('hemlock.view_survey'))
    _create_folders()
    _create_files(part)
    return send_file(
        os.getcwd()+'/tmp/survey_view.zip', mimetype='zip',
        attachment_filename='survey_view.zip', as_attachment=True)
    
# Get requested participant
def _get_participant():
    pid = request.form.get(list(request.form)[0])
    try:
        pid = int(pid)
    except:
        return
    return Participant.query.get(pid)

# Create and clean folders for the survey_view zip file
def _create_folders():
    tmpdir = 'tmp' if os.getcwd()=='/app' else '/tmp'
    try:
        os.mkdir(tmpdir)
    except:
        pass
    os.chdir('tmp')
    try:
        os.remove('survey_view.zip')
    except:
        pass
    os.chdir('..')
        
# Create png and docx files and zip
def _create_files(part):
    page_html, css, config = _setup_pages(part)
    
    os.chdir('tmp')
    doc = Document()
    zipf = zipfile.ZipFile('survey_view.zip', 'w', zipfile.ZIP_DEFLATED)
    [_process_page(i, p, css, config, doc, zipf) 
        for i, p in enumerate(page_html)]
    doc.save('survey_view.docx')
    zipf.write('survey_view.docx')
    os.remove('survey_view.docx')
    zipf.close()
    os.chdir('..')

# Set up for creating survey view files
# render page html and get css and config for imgkit
def _setup_pages(part):
    page_html = [render_template('survey_view.html', page=Markup(p))
        for p in part._page_html]
    dir = os.getcwd()
    css = [dir+url_for('static', filename='css/'+css_file)
        for css_file in ['default.min.css', 'bootstrap.min.css']]
    try:
        config = imgkit.config(wkhtmltoimage='/app/bin/wkhtmltoimage')
    except:
        config = imgkit.config()
    return page_html, css, config

# Process page
# create png file
# add to docx
# add to zip file
def _process_page(i, page, css, config, doc, zipf):
    page_name = 'page{}.png'.format(i)
    imgkit.from_string(
        page, page_name, css=css, config=config, options={'quiet':''})
    doc.add_picture(page_name, width=SURVEY_VIEW_IMG_WIDTH)
    zipf.write(page_name)
    os.remove(page_name)
    
    
    
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
    Question(p, 'Password', qtype='free')
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