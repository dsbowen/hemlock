"""Participant database models

Relationships:

branch_stack: stack of branches to be displayed
current_branch: head of the branch stack
current_page: head of the page queue of the current branch
pages: all Pages belonging to the Participant
question: all Questions belonging to the Participant
    
Columns:

g: Participant dictionary
meta: dictionary of Participant metadata
updated: indicates Participant data has been updated since last store
"""
from hemlock.app.factory import db
from hemlock.database.models.branch import Branch

from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import Mutable, MutableType, MutableDictType


class Participant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    branch_stack = db.relationship(
        'Branch',
        backref='part',
        order_by='Branch.index',
        collection_class=ordering_list('index'),
        foreign_keys='Branch._part_id'
        )
        
    current_branch = db.relationship(
        'Branch',
        uselist=False,
        foreign_keys='Branch._part_head_id'
        )
    
    @property
    def current_page(self):
        return self.current_branch.current_page
        
    @property
    def pages(self):
        return [p for b in self.branch_stack for p in b.pages]
        
    @property
    def questions(self):
        return [q for b in self.branch_stack for q in b.questions]
    
    # _page_htmls = db.relationship(
        # 'PageHtml',
        # backref='part',
        # lazy='dynamic'
        # )
    
    g = db.Column(MutableDictType)
    meta = db.Column(MutableDictType)
    updated = db.Column(db.Boolean)
    
    def __init__(self, start, meta={}): 
        db.session.add(self)
        db.session.flush([self])
        
        self.g = {}
        self.meta = {
            'end_time': datetime.utcnow(),
            'start_time': datetime.utcnow(),
            'status': 'in progress'
            }
        self.meta.update(meta)
        self.updated = True
        
        root = Branch(navigate=start)
        self.branch_stack.append(root)
        self.current_branch = root
        self._forward_recurse()

    def update_end_time(self):
        self.meta['end_time'] = datetime.utcnow()
    
    """Forward navigation"""
    def _forward(self, forward_to=None):
        """Advance forward to specified Page"""
        if forward_to is None:
            return self._forward_one()
        while self.current_page.id != forward_to.id:
            self._forward_one()
    
    def _forward_one(self):
        """Advance forward one page"""
        if self.current_page._eligible_to_insert_branch():
            self._insert_branch(self.current_page)
        else:
            self.current_branch._forward()
        self._forward_recurse()
    
    def _insert_branch(self, origin):
        """Grow and insert new Branch to branch_stack"""
        next_branch = origin._grow_branch()
        self.branch_stack.insert(self.current_branch.index+1, next_branch)
        self._increment_head()
        
    def _forward_recurse(self):
        """Recursive forward function
        
        Advance forward until the next Page is found (i.e. is not None).
        """
        if self.current_page is not None:
            return
        if self.current_branch._eligible_to_insert_branch():
            self._insert_branch(self.current_branch)
        else:
            self._decrement_head()
            self.current_branch._forward()
        self._forward_recurse()
    
    """Backward navigation"""
    def _back(self, back_to=None):
        """Navigate backward to specified Page"""
        if back_to is None:
            return self._back_one()
        while self.current_page.id != back_to.id:
            self._back_one()
            
    def _back_one(self):
        """Navigate backward one Page"""      
        if self.current_page == self.current_branch.start_page:
            self._remove_branch()
        else:
            self.current_branch._back()
        self._back_recurse()
        
    def _remove_branch(self):
        """Remove current branch from the branch stack"""
        self._decrement_head()
        self.branch_stack.pop(self.current_branch.index+1)
        
    def _back_recurse(self):
        """Recursive back function
        
        Navigate backward until previous Page is found.
        """
        if self._found_previous_page():
            return
        if self.current_page is None:
            if self.current_branch.next_branch in self.branch_stack:
                self._increment_head()
            elif not self.current_branch.pages:
                self._remove_branch()
            else:
                self.current_branch._back()
        else:
            self._increment_head()
        self._back_recurse()
    
    def _found_previous_page(self):
        """Indicate that previous page has been found in backward navigation
        
        The previous page has been found when 1) the Page is not None and
        2) it does not branch off to another Branch in the stack.
        """
        return (
            self.current_page is not None 
            and self.current_page.next_branch not in self.branch_stack
            )

    def _increment_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index+1]
    
    def _decrement_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index-1]
    
    def view_nav(self):
        """Print branch stack for debugging purposes"""
        self.branch_stack[0].view_nav()