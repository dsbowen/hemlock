from flask import render_template, redirect, url_for, session, request, Markup, make_response, request
from hemlock import app, db
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable
import io
import csv

from survey import Start #

@app.route('/')
def index():
    db.create_all()
    
    part = Participant()
    session['part_id'] = part.id
    
    root = Branch(part=part, next=Start)
    part.advance_page()
    db.session.commit()
    
    return redirect(url_for('survey'))
    
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
    
@app.route('/download')
def download():
    column = {}
    num_rows = 0
    
    participants = Participant.query.all()
    for part in participants:
        vars = Variable.query.filter_by(part_id=part.id).all()
        for var in vars:
            if var.name not in column:
                column[var.name] = [''] * num_rows
            column[var.name] += var.data
        num_rows += part.num_rows
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(column.keys())
    export_data = zip(*list(column.values()))
    cw.writerows(export_data)
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    output.headers['Context-type'] = 'text/csv'
    return output