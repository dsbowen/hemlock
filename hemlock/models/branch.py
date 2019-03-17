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
        
    _origin_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _origin_branch = db.relationship(
        'Branch',
        back_populates='_next_branch',
        uselist=False,
        foreign_keys=_origin_branch_id)
        
    _next_branch = db.relationship(
        'Branch',
        back_populates='_origin_branch',
        uselist=False,
        remote_side=id,
        foreign_keys=_origin_branch_id)
        
    _origin_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _origin_page = db.relationship(
        'Page', 
        back_populates='_next_branch',
        foreign_keys=_origin_page_id)
        
    _embedded = db.relationship(
        'Question', 
        backref='_branch', 
        lazy='dynamic',
        order_by='Question._index')
        
    _next_function = db.Column(db.PickleType)
    _next_args = db.Column(db.PickleType)
    
    # Add to database and commit upon initialization
    def __init__(self, next=None, next_args=None, randomize=False):
        db.session.add(self)
        db.session.commit()
        
        self.next(next, next_args)
        
    # Assign branch to participant
    # also assign embedded data
    def participant(self, participant=current_user, index=None):
        self._assign_parent(participant, '_part', index)
        [q.participant(participant) for q in self._embedded]
        
    # Remove branch from participant
    # als remove embedded data
    def remove_participant(self):
        self._remove_parent('_part')
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
        
    # Initialize head pointer to page in queue at given index
    def _initialize_head_pointer(self, index=0):
        if self._page_queue.all():
            self._current_page = self._page_queue.all()[index]
            return True
        self._current_page = None
        return False
        
    # Return to previous page
    def _back(self):
        if self._current_page == self._page_queue.first():
            return False
        if self._current_page is None:
            return self._initialize_head_pointer(-1)
        self._decrement_head()
        return True
        
    # Decrements the head pointer to previous page in queue
    def _decrement_head(self):
        new_head_index = self._current_page._index - 1
        self._current_page = self._page_queue[new_head_index]
        
    # Indicates whether the branch is eligible to grow and insert next branch
    # next function must not be None
    # and the next branch must not already be in the participant's branch stack
    def _eligible_to_insert_next(self):
        return (self._next_function is not None
            and self._next_branch not in self._part._branch_stack)
        
    # Print page queue
    def _print_page_queue(self):
        for p in self._page_queue.all():
            if p == self._current_page:
                print(p, '***')
            else:
                print(p)
        if self._current_page is None:
            print(None, '***')