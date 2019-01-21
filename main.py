from hemlock import app, db
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'Participant': Participant, 'Branch': Branch, 'Page': Page, 'Question': Question, 'Variable': Variable}