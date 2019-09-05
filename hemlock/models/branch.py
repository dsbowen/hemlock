##############################################################################
# Branch model
# by Dillon Bowen
# last modified 09/04/2019
##############################################################################

from hemlock.factory import db
from hemlock.models.private.base import Base
from flask_login import current_user



'''
Relationships:
    part: participant to whose branch stack this branch belongs
    page_queue: queue of pages to be displayed
    current_page: head of page queue
    origin_branch: parent branch from which this branch originated
    next_branch: child branch which originated from this branch
    origin_page: parent page from which this branch originated
    embedded: set of embedded data questions

Columns:
    next_function: navigation function which grows the next branch
    next_args: arguments for next function
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
    
    
    
    # Initialize branch
    def __init__(self, next=None, next_args=None):
        db.session.add(self)
        db.session.flush([self])
        
        self.next(next, next_args)
        
        
        
    ##########################################################################
    # Public methods
    ##########################################################################
        
    # PARTICIPANT
    # Assign branch to participant
    # also assign embedded data
    def participant(self, participant=current_user, index=None):
        self._assign_parent(participant, '_part', index)
        [q.participant(participant) for q in self._embedded.all()]
        
    # Get participant
    def get_participant(self):
        return self._part
        
    # Remove branch from participant
    # also remove embedded data
    def remove_participant(self):
        self._remove_parent('_part')
        [q.remove_participant() for q in self._embedded.all()]
        
        
    # PAGE QUEUE
    # Get the page queue
    def get_page_queue(self):
        return self._page_queue.all()
        
    # Clear the page queue
    def clear_page_queue(self):
        self._current_page = None
        self._remove_children('_page_queue')
        
        
    # ORIGIN AND NEXT BRANCH
    # Return the branch origin (may be branch or page)
    def get_origin(self):
        if self._origin_branch is not None:
            return self._origin_branch
        return self._origin_page
        
    # Return the next branch
    def get_next_branch(self):
        return self._next_branch
        
        
    # EMBEDDED QUESTIONS (DATA)
    # Return embedded questions (data)
    def get_embedded(self):
        return self._embedded
        
    # Clear embedded questions (data)
    def clear_embedded(self):
        self._remove_children('_embedded')
        
        
    # NEXT FUNCTION AND ARGUMENTS
    # Set the next navigation function and arguments
    # to clear next function and args: next()
    def next(self, next=None, args=None):
        self._set_function('_next_function', next, '_next_args', args)
        
    # Get the next function
    def get_next(self):
        return self._next_function
        
    # Get the next function arguments
    def get_next_args(self):
        return self._next_args
        
        
    # RANDOMIZATION
    # Randomize order of pages in queue
    def randomize(self):
        self._randomize_children('_page_queue')
        
        
        
    ##########################################################################
    # Navigation functions
    ##########################################################################
        
    # Advance to the next page in queue
    def _forward(self):
        if self._current_page is None:
            return
        new_head_index = self._current_page._index + 1
        if new_head_index == len(self._page_queue.all()):
            self._current_page = None
            return
        self._current_page = self._page_queue[new_head_index]
        
    # Return to previous page in queue
    def _back(self):
        if not self._page_queue:
            return
        if self._current_page is None:
            self._current_page = self._page_queue.all()[-1]
            return
        new_head_index = self._current_page._index - 1
        self._current_page = self._page_queue[new_head_index]
        
    # Initialize head pointer to first page in queue
    def _initialize_head_pointer(self):
        self._current_page = self._page_queue.first()
        
    # Print page queue
    # for debugging purposes only
    def _print_page_queue(self):
        for p in self._page_queue.all():
            if p == self._current_page:
                print(p, '***')
            else:
                print(p)
        if self._current_page is None:
            print(None, '***')