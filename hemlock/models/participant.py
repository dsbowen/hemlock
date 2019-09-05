##############################################################################
# Participant model
# by Dillon Bowen
# last modified 09/03/2019
##############################################################################

from hemlock.factory import db, login
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.private.page_html import PageHtml
from hemlock.models.question import Question
from hemlock.models.private.base import Base
from flask import request
from flask_login import UserMixin, login_user
from datetime import datetime
from copy import deepcopy



##############################################################################
# Login participant
##############################################################################

@login.user_loader
def load_user(id):
    return Participant.query.get(int(id))



'''
Relationships:
    branch_stack: stack of branches to be displayed
    current_branch: head of the branch stack
    pages: set of pages belonging to the participant
    page_htmls: set of page_htmls belonging to the participant
    questions: set of questions belonging to the participant
    variables: set of variables participant contributes to dataset
    
Columns:
    data: dictionary of data participant contributes to dataset
    g: global dictionary, accessible from navigation functions
    num_rows: number of rows participant contributes to dataset
    metadata: participant metadata (e.g. start and end time)
    page_html: html of all pages seen by participant
'''
class Participant(db.Model, UserMixin, Base):
    id = db.Column(db.Integer, primary_key=True)
    ds_completed_id = db.Column(db.Integer, db.ForeignKey('data_store.id'))
    ds_incomplete_id = db.Column(db.Integer, db.ForeignKey('data_store.id'))
    
    _branch_stack = db.relationship(
        'Branch',
        backref='_part',
        lazy='dynamic',
        order_by='Branch._index',
        foreign_keys='Branch._part_id')
        
    _current_branch = db.relationship(
        'Branch',
        uselist=False,
        foreign_keys='Branch._part_head_id')
        
    _pages = db.relationship(
        'Page',
        backref='_part',
        lazy='dynamic')
    
    _page_htmls = db.relationship(
        'PageHtml',
        backref='part',
        lazy='dynamic')
    
    _questions = db.relationship(
        'Question', 
        backref='_part', 
        lazy='dynamic',
        order_by='Question._part_index')
    
    _data = db.Column(db.PickleType)
    _g = db.Column(db.PickleType, default={})
    _num_rows = db.Column(db.Integer, default=0)
    _metadata = db.Column(db.PickleType, default={})
    
    
    
    # Initialize participant
    # login user
    # record metadata
    # initialize branch stack with root branch
    def __init__(self, ipv4, start): 
        
        db.session.add(self)
        db.session.flush([self])
        login_user(self)
        
        self._record_metadata(ipv4)
        
        root = Branch(next=start)
        root.participant()
        self._current_branch = root
        self._forward_recurse()
            
        db.session.commit()
        
        
        
    ##########################################################################
    # Global dictionary
    ##########################################################################
    
    # Modify participant's global dictionary
    # modification is a dictionary
    def modg(self, modification):
        temp = deepcopy(self._g)
        for key,value in modification.items():
            temp[key]=value
        self._g = deepcopy(temp)
    
    # Inspect participant's global dictionary
    # to_get may be list, dictionary, or key
    # nested lists and dictionaries are allowed
    def g(self, to_get):
        if type(to_get) is list:
            return [self.g(x) for x in to_get]
        if type(to_get) is dict:
            return {key:self.g(val) for (key,val) in to_get.items()}
        if to_get in self._g.keys():
            return deepcopy(self._g[to_get])


    
    ##########################################################################
    # Metadata
    ##########################################################################
    
    # Get metadata
    def get_metadata(self):
        return self._metadata
    
    # Record participant metadata
    def _record_metadata(self, ipv4):
        self._metadata = deepcopy({
            'id': self.id,
            'ipv4': ipv4,
            'start_time': datetime.utcnow(),
            'end_time': datetime.utcnow(),
            'completed': 0})
        
    # Update metadata (end time and completed indicator)
    def _update_metadata(self, completed=False):
        temp = deepcopy(self._metadata)
        temp['end_time'] = datetime.utcnow()
        temp['completed'] = int(completed)
        self._metadata = deepcopy(temp)
    
    
    
    ##########################################################################
    # Forward navigation
    ##########################################################################
    
    # Advance forward to specified page (forward_to)
    # assign new current branch to participant if terminal
    def _forward(self, forward_to_id=None):
        self._forward_one()
        if forward_to_id is not None:
            current_page = self._get_current_page()
            while current_page.id != forward_to_id:
                self._forward(current_page._forward_to_id)
                current_page = self._get_current_page()
                
        new_current_page = self._get_current_page()
        if new_current_page._terminal:
            new_current_page.participant()
    
    # Advance forward one page
    def _forward_one(self):
        current_page = self._get_current_page()
        current_page.participant()
        
        if current_page._eligible_to_insert_next():
            return self._insert_branch(current_page)
        self._current_branch._forward()
        self._forward_recurse()
    
    # Inserts a branch created by the origin
    # origin may be a page or branch
    def _insert_branch(self, origin):
        new_branch = origin._grow_branch()
        new_branch.participant(index=self._current_branch._index+1)
        self._increment_head()
        self._forward_recurse()
        
    # Recursive forward function
    # move through survey pages until it finds the next page
    def _forward_recurse(self):
        current_page = self._get_current_page()
        
        if current_page is None:
            if self._current_branch._eligible_to_insert_next():
                self._insert_branch(self._current_branch)
            else:
                self._decrement_head()
                self._current_branch._forward()
            return self._forward_recurse()
        
        
        
    ##########################################################################
    # Backward navigation
    ##########################################################################
    
    # Return back to specified page (back_to)
    def _back(self, back_to_id=None):
        self._back_one()
        if back_to_id is not None:
            current_page = self._get_current_page()
            while current_page.id != back_to_id:
                self._back(current_page._back_to_id)
                current_page = self._get_current_page()
            
    # Go back one page
    def _back_one(self):
        current_page = self._get_current_page()
        current_page.remove_participant()
        
        if current_page == self._current_branch._page_queue.first():
            return self._remove_branch()
        self._current_branch._back()
        self._back_recurse()
        
    # Remove the current branch from stack
    def _remove_branch(self):
        current_head_index = self._current_branch._index
        self._current_branch.remove_participant()
        self._decrement_head(current_head_index)
        self._back_recurse()
        
    # Recursive back function
    # move through survey pages until it finds the previous page
    def _back_recurse(self):
        current_page = self._get_current_page()
        
        if current_page is None:
            if self._current_branch._next_branch in self._branch_stack.all():
                self._increment_head()
            elif self._current_branch._page_queue.all():
                self._current_branch._back()
            else:
                return self._remove_branch()
            return self._back_recurse()
            
        if current_page._next_branch not in self._branch_stack.all():
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