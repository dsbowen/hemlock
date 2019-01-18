from hemlock import db
from hemlock.models.branch import Branch

class Participant(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	branch_stack = db.relationship('Branch', backref='part', lazy='dynamic')
	
	def get_branch(self):
		try:
			return self.branch_stack[-1]
		except:
			return None
			
	def remove_branch(self, branch):
		self.branch_stack.remove(branch)