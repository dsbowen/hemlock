##############################################################################
# Branch model
# by Dillon Bowen
# last modified 09/07/2019
##############################################################################

from hemlock.factory import attr_settor, db
from hemlock.models.private.base import Base, iscallable
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list



'''
Relationships:
    part: participant to whose branch stack this branch belongs
    pages: queue of pages to be displayed
    _current_page: head of page queue
    origin_branch: parent branch from which this branch originated
    next_branch: child branch which originated from this branch
    origin_page: parent page from which this branch originated
    embedded: list of embedded data questions

Columns:
    next_function: navigation function which grows the next branch
    next_args: arguments for next function
'''
class Branch(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _part_head_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _index = db.Column(db.Integer)
    
    pages = db.relationship(
        'Page', 
        backref='_branch', 
        order_by='Page.index',
        collection_class=ordering_list('index'),
        foreign_keys='Page._branch_id'
        )
        
    _current_page = db.relationship(
        'Page', 
        uselist=False,
        foreign_keys='Page._branch_head_id'
        )
        
    _origin_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    origin_branch = db.relationship(
        'Branch',
        back_populates='next_branch',
        uselist=False,
        foreign_keys=_origin_branch_id
        )
        
    next_branch = db.relationship(
        'Branch',
        back_populates='origin_branch',
        uselist=False,
        remote_side=id,
        foreign_keys=_origin_branch_id
        )
        
    _origin_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    origin_page = db.relationship(
        'Page', 
        back_populates='next_branch',
        foreign_keys=_origin_page_id
        )
        
    embedded = db.relationship(
        'Question', 
        backref='branch',
        order_by='Question.index',
        collection_class=ordering_list('index')
        )
        
    next = db.Column(db.PickleType)
    next_args = db.Column(db.PickleType)
    
    
    
    # Initialization
    def __init__(self, next=None, next_args={}):
        db.session.add(self)
        db.session.flush([self])
        
        self.next, self.next_args = next, next_args
        
        
        
    ##########################################################################
    # Navigation functions
    ##########################################################################
        
    # Advance to the next page in queue
    def _forward(self):
        if self._current_page is None:
            return
        new_head_index = self._current_page.index + 1
        if new_head_index == len(self.pages):
            self._current_page = None
            return
        self._current_page = self.pages[new_head_index]
        
    # Return to previous page in queue
    def _back(self):
        if not self.pages:
            return
        if self._current_page is None:
            self._current_page = self.pages[-1]
            return
        new_head_index = self._current_page.index - 1
        self._current_page = self.pages[new_head_index]
        
    # Initialize head pointer to first page in queue
    def _initialize_head_pointer(self):
        self._current_page = self.pages[0]
        
    # Print page queue
    # for debugging purposes only
    def _print_page_queue(self):
        for p in self.pages:
            if p == self._current_page:
                print(p, '***')
            else:
                print(p)
        if self._current_page is None:
            print(None, '***')
            
# Validate function attributes are callable (or None)
@attr_settor.register(Branch, 'next')
def valid_function(branch, value):
    return iscallable(value)