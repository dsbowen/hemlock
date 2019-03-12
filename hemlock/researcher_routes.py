###############################################################################
# Researcher URL routes for Hemlock survey
# by Dillon Bowen
# last modified 03/11/2019
###############################################################################

# hemlock database, application blueprint, and models
from hemlock.factory import db, bp
from hemlock.models import Participant, Page, Question

# flask functions
from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request
from flask_login import login_required, current_user, login_user

# other tools
from werkzeug.security import check_password_hash
from datetime import datetime
import io
import csv
import pandas as pd

'''
Download data
get data from all participants
write to csv and output
'''
@bp.route('/download', methods=['GET','POST'])
def download():
    p = Page()
    q = Question(p, 'Password', 'free')
    
    password = ''
    if request.method == 'POST':
        password = request.form.get(list(request.form)[0])
    if not check_password_hash(current_app.password_hash, password):
        return render_template('page.html', page=Markup(p._compile_html()))
    
    # get main dataframe
    data = pd.concat([pd.DataFrame(p.get_data()) 
        for p in Participant.query.all()], sort=False)
    
    # write to csv and output
    resp = make_response(data.to_csv(index_label='index'))
    resp.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    resp.headers['Content-Type'] = 'text/csv'
    return resp
    
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
        return render_template('page.html', page=Markup(p._compile_html()))
        
    ipv4 = current_app.ipv4_csv + current_app.ipv4_current
    ipv4 = pd.DataFrame.from_dict({'ipv4':ipv4})
    resp = make_response(ipv4.to_csv(index_label='index'))
    resp.headers['Content-Disposition'] = 'attachment; filename=block.csv'
    resp.headers['Content-Type'] = 'text/csv'
    return resp
    