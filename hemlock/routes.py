from flask import render_template, redirect, url_for, session, request, Markup, make_response, request
from hemlock import app, db
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
import io
import csv
import survey as Survey

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
    
    if request.method == 'POST':
        # validate
        # reload page if invalid
        # if valid, record responses and continue
        return redirect(url_for('survey'))
    
    branch = part.get_branch()
    if branch is None:
        return render_template('page.html', end_message=Markup(Survey.end()))
        
    page = branch.dequeue()
    if page is None:
        return terminate_branch(part, branch)
        
    db.session.commit()
    # session['page_id'] = page.id
    return render_template('page.html', page=Markup(page.render()))
    
def terminate_branch(part, branch):
    next = branch.get_next()
    part.remove_branch(branch)
    if next is not None:
        new_branch = getattr(Survey, next)()
        new_branch.part = part
    db.session.commit()
    return redirect(url_for('survey'))
	
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