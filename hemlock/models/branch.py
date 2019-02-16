###############################################################################
# Branch model
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

from hemlock import db
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.base import Base

'''
Data:
_part_id: ID of participant to whom the branch belongs
_page_queue: Queue of pages to render
_embedded: Set of embedded data questions
_next_function: next navigation function
_next_args: arguments for the next navigation function
_id_next: ID of the next branch
_randomize: indicator of page randomization
'''
class Branch(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    _page_queue = db.relationship('Page', backref='_branch', lazy='dynamic')
    _embedded = db.relationship('Question', backref='_branch', lazy='dynamic')
    _next_function = db.Column(db.PickleType)
    _next_args = db.Column(db.PickleType)
    _id_next = db.Column(db.Integer)
    _randomize = db.Column(db.Boolean)
    
    # Add to database and commit upon initialization
    def __init__(self, next=None, next_args=None, randomize=False):
        self._add_commit()
        self.next(next, next_args)
        self.randomize(randomize)
        
    # Set the next navigation function and arguments
    def next(self, next=None, args=None):
        self._set_function('_next_function', next, '_next_args', args)
        
    # Set page randomization on/off (True/False)
    def randomize(self, randomize=True):
        self._set_randomize(randomize)
        
    # Return the id of the next branch
    def get_next_branch_id(self):
        return self._id_next
        
    # Get page ids
    def _get_page_ids(self):
        return [page.id for page in self._page_queue.order_by('_order')]