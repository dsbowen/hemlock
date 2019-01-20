from hemlock import db
from hemlock.models.page import Page

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    page_queue = db.relationship('Page', backref='branch', lazy='dynamic')
    next = db.Column(db.PickleType)
    args = db.Column(db.PickleType)
    
    def dequeue(self):
        if not self.page_queue.all():
            return None
        page = self.page_queue[0]
        self.page_queue.remove(page)
        return page
        
    def set_next(self, next):
        self.next = next
        
    def set_args(self, args):
        self.args = args
        
    def get_next(self):
        if self.next:
            if self.args:
                return self.next(self.args)
            return self.next()
        return None