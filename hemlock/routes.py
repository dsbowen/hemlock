from hemlock import app, db
import survey

@app.route('/')
def index():
    db.create_all()
    db.session.add(survey.q)
    db.session.commit()
    return survey.q.text