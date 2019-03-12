###############################################################################
# Branch model
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

from hemlock.factory import db
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.private.base import Base

'''
Data:
_part_id: ID of participant to whom the branch belongs
_page_queue: Queue of pages to render
_embedded: List of embedded data questions
_next_function: next navigation function
_next_args: arguments for the next navigation function
_id_next: ID of the next branch
'''
class Branch(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    _page_queue = db.relationship('Page', backref='_branch', lazy='dynamic',
        order_by='Page._order')
    _embedded = db.relationship('Question', backref='_branch', lazy='dynamic',
        order_by='Question._order')
    _next_function = db.Column(db.PickleType)
    _next_args = db.Column(db.PickleType)
    _id_next = db.Column(db.Integer) # SHOULD HAVE 1:1 RELATIONSHIP
    
    # Add to database and commit upon initialization
    def __init__(self, next=None, next_args=None, randomize=False):
        db.session.add(self)
        db.session.commit()
        
        self.next(next, next_args)
        
    # Set the next navigation function and arguments
    def next(self, next=None, args=None):
        self._set_function('_next_function', next, '_next_args', args)
        
    # Randomize page order
    def randomize(self):
        self._randomize_children(self._page_queue.all())
        
    # Return the id of the next branch
    def get_next_branch_id(self):
        return self._id_next
        
    # Get page ids
    def _get_page_ids(self):
        return [page.id for page in self._page_queue]