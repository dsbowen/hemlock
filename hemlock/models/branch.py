###############################################################################
# Branch model
# by Dillon Bowen
# last modified 03/16/2019
###############################################################################

from hemlock.factory import db
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.private.base import Base
from flask_login import current_user

'''
Data:
_page_queue: Queue of pages to render
_embedded: List of embedded data questions
_next_function: next navigation function
_next_args: arguments for the next navigation function
_id_next: ID of the next branch
'''
class Branch(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _part_head_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _index = db.Column(db.Integer)
    
    _page_queue = db.relationship(
        'Page', 
        backref='_branch', 
        lazy='dynamic',
        order_by='Page._index',
        foreign_keys='Page._branch_id')
        
    _current_page = db.relationship(
        'Page', 
        uselist=False,
        foreign_keys='Page._branch_head_id')
        
    _next_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _next_branch = db.relationship(
        'Branch', 
        uselist=False,
        foreign_keys=[_next_branch_id])
        
    _embedded = db.relationship('Question', backref='_branch', lazy='dynamic',
        order_by='Question._order')
    _next_function = db.Column(db.PickleType)
    _next_args = db.Column(db.PickleType)
    
    # Add to database and commit upon initialization
    def __init__(self, next=None, next_args=None, randomize=False):
        db.session.add(self)
        db.session.commit()
        
        self.next(next, next_args)
        
    # Assign embedded data to participant
    def participant(self, participant=current_user):
        [q.participant(participant) for q in self._embedded]
        
    # Remove embedded data from participant
    def remove_participant(self):
        [q.remove_participant() for q in self._embedded]
        
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
        
        
        
    ###########################################################################
    # Navigation
    ###########################################################################
        
    # Advance to the next page
    def _forward(self):
        if self._current_page is None:
            return
        self._advance_head()
        
    # Advances head pointer to next page in queue
    def _advance_head(self):
        new_head_index = self._current_page._index + 1
        if new_head_index == len(self._page_queue.all()):
            self._current_page = None
            return
        self._current_page = self._page_queue[new_head_index]
        
    # Grow and return a new branch
    def _grow_branch(self):
        next_branch = self._call_function(
            function=self._next_function, 
            args=self._next_args)

        if next_branch is None:
            return
        
        next_branch._initialize_head_pointer()
        return next_branch
        
    # Initialize head pointer to first page in queue
    def _initialize_head_pointer(self):
        print(self)
        print(self._page_queue.all())
        if self._page_queue.all():
            self._current_page = self._page_queue.first()
            return
        self._current_page = None