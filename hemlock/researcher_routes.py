###############################################################################
# Researcher URL routes for Hemlock survey
# by Dillon Bowen
# last modified 03/12/2019
###############################################################################

# hemlock database, application blueprint, and models
from hemlock.factory import db, bp
from hemlock.models import Participant, Page, Question
from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request, flash
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash
from datetime import datetime
import io
import csv
import pandas as pd



###############################################################################
# Main view functions
###############################################################################

# Download data
# collect participant responses in dataframe
# write to csv and output
@bp.route('/download')
def download():
    if not valid_password():
        return redirect(url_for('hemlock.password', requested_url='download'))
    
    data = pd.concat([pd.DataFrame(p.get_data()) 
        for p in Participant.query.all()], sort=False)
    resp = make_response(data.to_csv(index_label='index'))
    resp.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    resp.headers['Content-Type'] = 'text/csv'
    return resp
    
# Download list of ipv4 addresses
# for blocking duplicates in subsequent studies
@bp.route('/ipv4', methods=['GET','POST'])
def ipv4():
    if not valid_password():
        return redirect(url_for('hemlock.password', requested_url='ipv4'))
        
    ipv4 = current_app.ipv4_csv + current_app.ipv4_current
    ipv4 = pd.DataFrame.from_dict({'ipv4':ipv4}).drop_duplicates()
    resp = make_response(ipv4.to_csv(index=False))
    resp.headers['Content-Disposition'] = 'attachment; filename=block.csv'
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
    Question(p, 'Password', 'free')
    return render_template('page.html', page=Markup(p._compile_html()))
    