###############################################################################
# Researcher URL routes for Hemlock survey
# by Dillon Bowen
# last modified 04/05/2019
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
# Main view functions
###############################################################################

# Download data
# data: {'var_name':[entries]}
@bp.route('/download')
def download():
    if not valid_password():
        return redirect(url_for('hemlock.password', requested_url='download'))
    
    ds = DataStore.query.first()
    ds.store_on_download(record_incomplete=current_app.record_incomplete)
    
    return get_response(data=ds.data, filename='data')
    
# Download list of ipv4 addresses
# for blocking duplicates in subsequent studies
@bp.route('/ipv4', methods=['GET','POST'])
def ipv4():
    if not valid_password():
        return redirect(url_for('hemlock.password', requested_url='ipv4'))
        
    ipv4 = list(set(current_app.ipv4_csv + Visitors.query.first().ipv4))
    return get_response(data={'ipv4': ipv4}, filename='block')
    
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
    
    
    
###############################################################################
# Password validation
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
    