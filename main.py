from hemlock import app, db
from hemlock.models.question import Question

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'Question': Question}