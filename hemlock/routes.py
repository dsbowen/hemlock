from flask import make_response
from hemlock import app, db
from hemlock.models.question import Question
import io
import csv
import survey

@app.route('/')
def index():
    db.create_all()
    db.session.add(survey.q)
    db.session.commit()
    return survey.q.text
    
@app.route('/download')
def download():
    data = Question.query.get(1).text
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow([data])
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    output.headers['Context-type'] = 'text/csv'
    return output
    # with open('test.csv', 'w') as test_file:
        # x = csv.writer(test_file, delimiter=' ', quotechar='|', quoting = csv.QUOTE_MINIMAL)
        # x.writerow(['hello world'])
        # return Response(test_file, mimetype='text/csv')
        # return send_file(test_file, mimetype='text/csv', attachment_filename='test.csv', as_attachment=True)
    # return data