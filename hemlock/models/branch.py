###############################################################################
# Branch model
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import db
from hemlock.models.page import Page

# Data:
# ID of participant to whom the branch belongs
# Queue of pages to render
# Next: pointer to the next navigation function
# Arguments for the next navigation function
class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    page_queue = db.relationship('Page', backref='branch', lazy='dynamic')
    next = db.Column(db.PickleType)
    args = db.Column(db.PickleType)
    
    # Add branch to database and commit upon initialization
    def __init__(self, part=None, next=None):
        self.part = part
        self.set_next(next)
        db.session.add(self)
        db.session.commit()
    
    # Dequeue a page
    def dequeue(self):
        if not self.page_queue.all():
            return None
        page = self.page_queue.order_by('order').first()
        self.remove_page(page)
        return page
        
    # Set a pointer to the next navigation function
    def set_next(self, next):
        self.next = next
        
    # Set the arguments for the next navigation function
    def set_args(self, args):
        self.args = args
        
    # Return the next branch by calling the next navigation function
    def get_next(self):
        if self.next:
            if self.args:
                return self.next(self.args)
            return self.next()
        return None
        
    # Remove a page from the page queue
    # reset order for remaining pages
    def remove_page(self, page):
        self.page_queue.remove(page)
        pages = self.page_queue.order_by('order')
        for i in range(len(self.page_queue.all())):
            pages[i].set_order(i)