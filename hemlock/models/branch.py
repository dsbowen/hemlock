from hemlock import db
from hemlock.models.page import Page

class Branch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
	page_queue = db.relationship('Page', backref='branch', lazy='dynamic')
	next = db.Column(db.Text)
	
	def dequeue(self):
		if not self.page_queue.all():
			return None
		page = self.page_queue[0]
		self.page_queue.remove(page)
		return page
			
	def get_next(self):
		if self.next:
			return self.next
		return None