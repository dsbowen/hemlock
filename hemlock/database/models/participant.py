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
status: in progress, completed, or timed out
updated: indicates Participant data has been updated since last store
"""
from hemlock.app.factory import db
from hemlock.database.private import DataStore
from hemlock.database.types import DataFrame
from hemlock.database.models.branch import Branch

from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import Mutable, MutableType, MutableDictType

def send_data(func):
    """Send data to the DataStore
    
    Begin by recording the Participant's previous status. If the status has
    changed as a result of the update, register the change in the DataStore.
    """
    def status_update(part, update):
        part.previous_status = part.status
        return_val = func(part, update)
        if part.previous_status == part.status:
            return return_val
        DataStore.query.first().update_status(part)
        return return_val
    return status_update


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
        questions = [q for b in self.branch_stack for q in b.questions]
        questions.sort(key=lambda q: q.id)
        return questions
    
    _page_htmls = db.relationship('PageHtml', backref='part', lazy='dynamic')
    
    g = db.Column(MutableDictType, default={})
    _completed = db.Column(db.Boolean, default=False)
    end_time = db.Column(db.DateTime)
    _meta = db.Column(MutableDictType, default={})
    previous_status = db.Column(db.String(16))
    updated = db.Column(db.Boolean, default=True)
    start_time = db.Column(db.DateTime)
    _time_expired = db.Column(db.Boolean, default=False)
    
    @property
    def completed(self):
        return self._completed
        
    @completed.setter
    @send_data
    def completed(self, completed):
        self._completed = completed
        
    @property
    def time_expired(self):
        return self._time_expired
        
    @time_expired.setter
    @send_data
    def time_expired(self, time_expired):
        self._time_expired = time_expired
    
    @property
    def status(self):
        if self.completed:
            return 'completed'
        if self.time_expired:
            return 'timed_out'
        return 'in_progress'
    
    def __init__(self, start_navigation, meta={}):
        """Initialize Participant
        
        Sets up the global dictionary g and metadata. Then initializes the
        root branch.
        """
        db.session.add(self)
        db.session.flush([self])
        DataStore.query.first().update_status(self)
        
        self.end_time = self.start_time = datetime.utcnow()
        self.meta = meta.copy()
        DataStore.query.first().meta.append(meta)
        
        self.current_branch = root = start_navigation()
        self.branch_stack.append(root)
        root.current_page = root.start_page
        root._isroot = True

    def update_end_time(self):
        self.end_time = datetime.utcnow()
    
    """Data packaging"""
    @property
    def meta(self):
        self._meta['ID'] = self.id
        self._meta['end_time'] = self.end_time
        self._meta['start_time'] = self.start_time
        self._meta['status'] = self.status
        return self._meta
        
    @meta.setter
    def meta(self, meta):
        self._meta = meta
    
    @property
    def data(self):
        """Participant data
        
        Note that Questions are added to the dataframe in the order in which 
        they were created (i.e. by id). This is not necessarily the order in 
        which they appeared to the Participant.
        """
        self.set_order_all()
        questions = self.questions
        df = DataFrame()
        df.add(data=self.meta, all_rows=True)
        [df.add(data=q._package_data(), all_rows=q.all_rows) 
            for q in questions]
        df.pad()
        return df
    
    def set_order_all(self):
        """Set the order for all Questions
        
        A Question's order is the order in which it appeared to the 
        Participant relative to other Questions of the same variable. These 
        functions walk through the survey and sets the Question order.
        
        Note that a Branch's embedded data Questions are set before its 
        Pages' Questions. A Page's timer is set before its Questions.
        """
        var_count = {}
        self.set_order_branch(self.branch_stack[0], var_count)
    
    def set_order_branch(self, branch, var_count):
        """Set the order for Questions belonging to a given Branch"""
        [self.set_order_question(q, var_count) for q in branch.embedded]
        [self.set_order_page(p, var_count) for p in branch.pages]
        if branch.next_branch in self.branch_stack:
            self.set_order_branch(branch.next_branch, var_count)
    
    def set_order_page(self, page, var_count):
        """Set the order for Questions belonging to a given Page"""
        questions = [page.timer]+page.questions
        [self.set_order_question(q, var_count) for q in questions]
        if page.next_branch in self.branch_stack:
            self.set_order_branch(page.next_branch, var_count)
        
    def set_order_question(self, question, var_count):
        """Set the order for a given Question"""
        var = question.var
        if var is None:
            return
        if var not in var_count:
            var_count[var] = 0
        question.order = var_count[var]
        var_count[var] += 1
    
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

    """General navigation and debugging"""
    def _increment_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index+1]
    
    def _decrement_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index-1]
    
    def view_nav(self):
        """Print branch stack for debugging purposes"""
        self.branch_stack[0].view_nav()