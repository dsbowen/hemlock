###############################################################################
# Branch model
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import db
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.base import Base

# Data:
# ID of participant to whom the branch belongs
# Queue of pages to render
# Set of embedded data questions
# Next: pointer to the next navigation function
# Arguments for the next navigation function
class Branch(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    page_queue = db.relationship('Page', backref='branch', lazy='dynamic')
    embedded = db.relationship('Question', backref='branch', lazy='dynamic')
    next = db.Column(db.PickleType)
    next_args = db.Column(db.PickleType)
    randomize = db.Column(db.Boolean)
    
    # Add branch to database and commit upon initialization
    def __init__(self, part=None, next=None, args=None, randomize=False):
        self.assign_participant(part)
        self.set_next(next, args)
        self.set_randomize(randomize)
        db.session.add(self)
        db.session.commit()
    
    # Dequeue a page
    def dequeue(self):
        if not self.page_queue.all():
            return None
        page = self.page_queue.order_by('order').first()
        page.remove_branch()
        return page
        
    # Set a pointer to the next navigation function
    def set_next(self, next=None, args=None):
        self.set_function('next', next, 'next_args', args)