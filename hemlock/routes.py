from hemlock import app, db
import survey

@app.route('/')
def index():
    return survey.q.text