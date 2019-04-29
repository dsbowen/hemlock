###############################################################################
# Researcher URL routes for Hemlock survey
# by Dillon Bowen
# last modified 04/14/2019
###############################################################################

# hemlock database, application blueprint, and models
from hemlock.factory import db, bp
from hemlock.models import Participant, Page, Question
from hemlock.models.private import DataStore, Visitors
from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request, flash
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
    
# Store data from participants who completed the survey
# but are not counted as completed in DataStore
# this occurs in rare cases when participants disconnect
# before the terminal page can load
@bp.route('/store_completed')
def store_completed():
    ds = DataStore.query.first()
    [ds.store(p) for p in Participant.query.all()
        if p.id not in ds.completed_ids and p._metadata['completed']]
    db.session.commit()
    return ''
        
# Data download
# this view called after store_completed
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