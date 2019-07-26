###############################################################################
# Researcher URL routes for Hemlock survey
# by Dillon Bowen
# last modified 07/26/2019
###############################################################################

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
import csv
import imgkit
import os
import zipfile




###############################################################################
# Data download views
###############################################################################

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



###############################################################################
# ipv4 download view
###############################################################################

# Download list of ipv4 addresses
# for blocking duplicates in subsequent studies
@bp.route('/ipv4', methods=['GET','POST'])
def ipv4():
    if not valid_password():
        return redirect(url_for('hemlock.password', requested_url='ipv4'))
        
    ipv4 = list(set(current_app.ipv4_csv + Visitors.query.first().ipv4))
    return get_response(data={'ipv4': ipv4}, filename='block')
    
@bp.route('/view_survey', methods=['GET','POST'])
def view_survey():
    if not valid_password():
        return redirect(url_for(
            'hemlock.password', requested_url='view_survey'))
    
    if request.method == 'POST':
        part_ids = [p.id for p in Participant.query.all()]
        part_id = int(request.form.get(list(request.form)[0]))
        if part_id in part_ids:
            return download_survey(part_id)
        # try:
            # part_id = int(request.form.get(list(request.form)[0]))
            # if part_id in part_ids:
                # return download_survey(part_id)
        # except:
            # pass

    p = Page()
    Question(p, 'Participant ID', qtype='free')
    return render_template('page.html', page=Markup(p._compile_html()))
    
def _view_survey(part_id):
    compiled_html = Participant.query.get(part_id)._page_html
    compiled_html = Markup('\n<hr>\n'.join(compiled_html))
    return render_template('page.html', page=compiled_html)
    
import pdfkit
def download_survey(part_id):
    compiled_html = Participant.query.get(part_id)._page_html
    rendered_html = [render_template('temp.html', page=Markup(html))
        for html in compiled_html]
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    css = [basedir+'/templates'+css_file 
        for css_file in ['/temp.css', '/bootstrap.min.css']]

    # images = [imgkit.from_string(html, False, css=css) 
        # for html in rendered_html]
    config = pdfkit.configuration(wkhtmltopdf=app.conifig['WKHTMLTOPDF_BINARY'])
    images = [pdfkit.from_string(html, False, css=css, configuration=config) 
        for html in rendered_html]
    
    zipf = zipfile.ZipFile('survey.zip', 'w', zipfile.ZIP_DEFLATED)
    [zipf.writestr('page{}.pdf'.format(i), img) 
        for i, img in enumerate(images)]
    zipf.close()
    return send_file(
        '../survey.zip', mimetype='zip', 
        attachment_filename='survey.zip', as_attachment=True)
    
    
    
###############################################################################
# Password validation and get response
###############################################################################

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