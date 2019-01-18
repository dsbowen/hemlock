from hemlock import db
from hemlock.models.question import Question
from random import choice
from string import ascii_letters, digits

def hidden_tag():
	tag = ''.join([choice(ascii_letters + digits) for i in range(90)])
	return "<input name='crsf_token' type='hidden' value='" + tag + "'>"

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
	questions = db.relation('Question', backref='page', lazy='dynamic')
	
	def assign_branch(self, branch):
		self.branch = branch
	
	def render(self):
		rendered_html = hidden_tag()
		for question in self.questions:
			rendered_html += question.render()
		rendered_html += "<p align=right><input type='submit' name='submit' value='>>'></p>"
		return rendered_html