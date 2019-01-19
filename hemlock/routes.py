from flask import render_template, redirect, url_for, session, request, Markup, make_response, request
from hemlock import app, db
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
import io
import csv

@app.route('/')
def index():
    db.create_all()
    
    part = Participant()
    db.session.add(part)
    db.session.commit()
    session['part_id'] = part.id
    
    root = Branch(part=part, next='start')
    db.session.commit()
    
    return redirect(url_for('survey'))
    
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    part = Participant.query.get(session['part_id'])
    part.advance_page()
    page = part.get_page()
    db.session.commit()
    return render_template('page.html', page=Markup(page.render()))
    
    # if request.method == 'POST':
        # validate
        # reload page if invalid
        # if valid, record responses and continue
        # return redirect(url_for('survey'))
    
@app.route('/download')
def download():
    # figure out how to download cleaned data
    data = Question.query.get(1).text
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow([data])
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    output.headers['Context-type'] = 'text/csv'
    return output