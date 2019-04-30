###############################################################################
# Researcher URL routes for Hemlock survey
# by Dillon Bowen
# last modified 04/14/2019
###############################################################################

# hemlock database, application blueprint, and models
from hemlock.factory import db, bp
from hemlock.models import Participant, Page, Question
from hemlock.models.private import DataStore, Visitors
from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request, flash, jsonify
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash
from datetime import datetime
from io import StringIO
import csv



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
import time
@bp.route('/_update_data_store')
def _update_data_store():
    ds = DataStore.query.first()
    return jsonify(finished=ds.update(current_app.record_incomplete))
        
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