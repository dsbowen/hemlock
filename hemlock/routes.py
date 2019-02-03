###############################################################################
# URL routes for Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from flask import current_app, render_template, redirect, url_for, session, request, Markup, make_response, request
from hemlock import db, bp
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable
import io
import csv
import pandas as pd

# Create participant and root branch before beginning survey
@bp.before_app_first_request
def before_app_first_request():
    db.create_all()
    
    part = Participant()
    session['part_id'] = part.id
    root = Branch(part=part, next=current_app.start)
    part.advance_page()

# Main survey route
# alternates between GET and POST
#   GET: render current page
#   POST: collect and validate responses, advance to next page
# stores participant data on terminal page
@bp.route('/', methods=['GET','POST'])
def index():
    part = Participant.query.get(session['part_id'])
    page = part.get_page()
        
    if page.validate_on_submit():
        part.advance_page()
        db.session.commit()
        return redirect(url_for('hemlock.index'))
        
    if page.terminal:
        page.render() # might change this when I record partial responses
        part.store_data()
        
    return render_template('page.html', page=Markup(page.render()))
    
# Download data
# gets data from all participants
# writes to csv
# outputs csv
@bp.route('/download')
def download():
    data = pd.concat([pd.DataFrame(p.data) for p in Participant.query.all()],
        sort=False)
    resp = make_response(data.to_csv())
    resp.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    resp.headers['Content-Type'] = 'text/csv'
    return resp
    