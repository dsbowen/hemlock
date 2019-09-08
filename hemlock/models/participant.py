##############################################################################
# Participant model
# by Dillon Bowen
# last modified 09/07/2019
##############################################################################

from hemlock.factory import attr_settor, db, login
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.private.page_html import PageHtml
from hemlock.models.question import Question
from hemlock.models.private.base import Base
from flask import request
from flask_login import UserMixin, login_user
from sqlalchemy.ext.orderinglist import ordering_list
from datetime import datetime



##############################################################################
# Login participant
##############################################################################

@login.user_loader
def load_user(id):
    return Participant.query.get(int(id))



'''
Relationships:
    _branch_stack: stack of branches to be displayed
    _current_branch: head of the branch stack
    _page_htmls: list of page_htmls belonging to the participant
    _variables: set of variables participant contributes to dataset
    
Columns:
    g: participant dictionary
    meta: participant metadata (e.g. start and end time)
    _data: dictionary of data participant contributes to dataset
    _num_rows: number of rows participant contributes to dataset
'''
class Participant(db.Model, UserMixin, Base):
    id = db.Column(db.Integer, primary_key=True)
    _ds_completed_id = db.Column(db.Integer, db.ForeignKey('data_store.id'))
    _ds_incomplete_id = db.Column(db.Integer, db.ForeignKey('data_store.id'))
    
    _branch_stack = db.relationship(
        'Branch',
        backref='part',
        order_by='Branch._index',
        collection_class=ordering_list('_index'),
        foreign_keys='Branch._part_id'
        )
        
    _current_branch = db.relationship(
        'Branch',
        uselist=False,
        foreign_keys='Branch._part_head_id'
        )
    
    _page_htmls = db.relationship(
        'PageHtml',
        backref='part',
        lazy='dynamic'
        )
    
    g = db.Column(db.PickleType)
    meta = db.Column(db.PickleType)
    
    _data = db.Column(db.PickleType)
    _num_rows = db.Column(db.Integer, default=0)
    
    
    
    # Initialization
    # login user
    # record meta
    # initialize branch stack with root branch
    def __init__(self, ipv4, start): 
        db.session.add(self)
        db.session.flush([self])
        login_user(self)
        
        self._init_meta(ipv4)
        
        root = Branch(next=start)
        self._branch_stack.append(root)
        self._current_branch = root
        self._forward_recurse()


    
    ##########################################################################
    # Metadata
    ##########################################################################
    
    # Initialize meta
    def _init_meta(self, ipv4):
        self.meta = {
            'id': self.id,
            'ipv4': ipv4,
            'start_time': datetime.utcnow(),
            'end_time': datetime.utcnow(),
            'completed': 0
            }
        
    # Update meta (end time and completed indicator)
    def _update_meta(self, completed=False):
        self.meta['end_time'] = datetime.utcnow()
        self.meta['completed'] = int(completed)
    
    
    
    ##########################################################################
    # Forward navigation
    ##########################################################################
    
    # Advance forward to specified page (forward_to)
    # assign new current branch to participant if terminal
    def _forward(self, forward_to_id=None):
        if forward_to_id is None:
            self._forward_one()
            return
        while self._get_current_page().id != forward_to_id:
            self._forward_one()
    
    # Advance forward one page
    def _forward_one(self):
        current_page = self._get_current_page()
        if current_page._eligible_to_insert_next():
            return self._insert_branch(current_page)
        self._current_branch._forward()
        self._forward_recurse()
    
    # Inserts a branch created by the origin
    # origin may be a page or branch
    def _insert_branch(self, origin):
        new_branch = origin._grow_branch()
        self._branch_stack.insert(self._current_branch._index+1, new_branch)
        self._increment_head()
        self._forward_recurse()
        
    # Recursive forward function
    # move through survey pages until next page is found
    def _forward_recurse(self):
        current_page = self._get_current_page()
        if current_page is None:
            if self._current_branch._eligible_to_insert_next():
                self._insert_branch(self._current_branch)
            else:
                self._decrement_head()
                self._current_branch._forward()
            self._forward_recurse()
        
        
        
    ##########################################################################
    # Backward navigation
    ##########################################################################

    # Return back to specified page (back_to)
    def _back(self, back_to_id=None):
        if back_to_id is None:
            self._back_one()
            return
        while self._get_current_page().id != back_to_id:
            self._back_one()
            
    # Go back one page
    def _back_one(self):
        current_page = self._get_current_page()        
        if current_page == self._current_branch.pages[0]:
            return self._remove_branch()
        self._current_branch._back()
        self._back_recurse()
        
    # Remove the current branch from stack
    def _remove_branch(self):
        current_head_index = self._current_branch._index
        self._branch_stack.remove(self._current_branch)
        self._decrement_head(current_head_index)
        self._back_recurse()
        
    # Recursive back function
    # move through survey pages until it finds the previous page
    def _back_recurse(self):
        current_page = self._get_current_page()
        if current_page is None:
            if self._current_branch._next_branch in self._branch_stack:
                self._increment_head()
            elif self._current_branch.pages:
                self._current_branch._back()
            else:
                return self._remove_branch()
            return self._back_recurse()
            
        if current_page._next_branch not in self._branch_stack:
            return
        self._increment_head()
        self._back_recurse()
        
        
    
    ##########################################################################
    # General navigation and debugging
    ##########################################################################
    
    # Return the current page
    def _get_current_page(self):
        return self._current_branch._current_page

    # Advance head pointer to next branch in stack
    def _increment_head(self):
        new_head_index = self._current_branch._index + 1
        self._current_branch = self._branch_stack[new_head_index]
            
    # Decrements head pointer to previous branch in stack
    def _decrement_head(self, head_index=None):
        if head_index is None:
            head_index = self._current_branch._index
        new_head_index = head_index - 1
        self._current_branch = self._branch_stack[new_head_index] 
        
    # Print branch stack
    def _print_branch_stack(self):
        for b in self._branch_stack.all():
            if b == self._current_branch:
                print(b, '***')
            else:
                print(b)
            b._print_page_queue()