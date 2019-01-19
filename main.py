from hemlock import app, db
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'Branch': Branch, 'Page': Page, 'Question': Question}