"""Participant database models

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

"""
from hemlock.app.factory import db#, login
from hemlock.database.models.branch import Branch

from datetime import datetime
from flask_login import UserMixin, login_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import Mutable, MutableType, MutableDictType

STATUS = ['in progress', 'timed out', 'completed']


# @login.user_loader
# def load_user(id):
    # return Participant.query.get(int(id))


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
    
    # _page_htmls = db.relationship(
        # 'PageHtml',
        # backref='part',
        # lazy='dynamic'
        # )
    
    g = db.Column(MutableType)
    end_time = db.Column(db.DateTime)
    ipv4 = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    _status = db.Column(db.String(16))
    updated = db.Column(db.Boolean)
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        assert status in STATUS, (
            'Participant status must be one of {}'.format(STATUS)
            )
        self._status = status
    
    _data = db.Column(db.PickleType)
    _num_rows = db.Column(db.Integer, default=0)
    
    def __init__(self, start, ipv4=None): 
        db.session.add(self)
        db.session.flush([self])
        # login_user(self)
        
        self.g = Mutable()
        self.end_time = self.start_time = datetime.utcnow()
        self.ipv4 = ipv4
        self.status = 'in progress'
        self.updated = True
        
        root = Branch(navigate=start)
        self.branch_stack.append(root)
        self.current_branch = root
        self._forward_recurse()

    def update_end_time(self):
        self.end_time = datatime.utcnow()
    
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
        return (
            self.current_page is not None 
            and self.current_page.next_branch not in self.branch_stack
            )

    def _increment_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index+1]
    
    def _decrement_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index-1]
    
    def _print(self):
        """Print branch stack for debugging purposes"""
        self.branch_stack[0]._print_navigation()