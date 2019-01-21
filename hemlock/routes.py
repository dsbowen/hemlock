###############################################################################
# URL routes for Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from flask import render_template, redirect, url_for, session, request, Markup, make_response, request
from hemlock import app, db
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable
import io
import csv

# GET RID OF THIS WHEN YOU MAKE APPLICATION FACTORY
from survey import Start #

# Initial survey route
# creates a new participant and root branch
@app.route('/')
def index():
    db.create_all()
    
    part = Participant()
    session['part_id'] = part.id
    
    root = Branch(part=part, next=Start)
    part.advance_page()
    db.session.commit()
    
    return redirect(url_for('survey'))
  
# Main survey route
# alternates between GET and POST
#   GET: render current page
#   POST: collect and validate responses, advance to next page
# stores participant data on terminal page
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    part = Participant.query.get(session['part_id'])
    page = part.get_page()
        
    if page.validate_on_submit():
        part.advance_page()
        db.session.commit()
        return redirect(url_for('survey'))
        
    if page.terminal:
        part.store_data()
        
    return render_template('page.html', page=Markup(page.render()))
    
# Download data
# gets data from all participants
# writes to csv
# outputs csv
@app.route('/download')
def download():
    data = get_data()

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(data.keys())
    export_data = zip(*list(data.values()))
    cw.writerows(export_data)
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    output.headers['Context-type'] = 'text/csv'
    return output
    
# Get data
# Creates a dictionary where key=variable name, value=[data]
def get_data():
    data = {}
    num_rows = 0
    
    participants = Participant.query.all()
    for part in participants:
        vars = Variable.query.filter_by(part_id=part.id).all()
        for var in vars:
            # Pad variable values if variable has not been seen before
            if var.name not in data:
                data[var.name] = [''] * num_rows
            data[var.name] += var.data
        num_rows += part.num_rows
    return data
    