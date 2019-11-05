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

from hemlock.app import db
from hemlock.database.private import Base, DataStore, Router
from hemlock.database.types import DataFrame

from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import MutableDictType

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


class Participant(UserMixin, Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    _router = db.relationship(
        'Router',
        backref='part',
        uselist=False
    )
    
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

    _forward_to_id = db.Column(db.Integer)
    g = db.Column(MutableDictType)
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
        ds = DataStore.query.first()
        ds.meta.append(meta)
        ds.update_status(self)

        self._router = Router()
        self.end_time = self.start_time = datetime.utcnow()
        self.meta = meta.copy()
        self.g = {}
        
        self.current_branch = root = start_navigation()
        self.branch_stack.append(root)
        root.current_page = root.start_page
        root.is_root = True
        
        super().__init__()

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
        print('about to setting order')
        self._set_order_all()
        questions = self.questions
        df = DataFrame()
        print('adding data to dataframe')
        df.add(data=self.meta, all_rows=True)
        [df.add(data=q._pack_data(), all_rows=q.all_rows) for q in questions]
        print('padding df')
        df.pad()
        return df
    
    def _set_order_all(self):
        """Set the order for all Questions
        
        A Question's order is the order in which it appeared to the 
        Participant relative to other Questions of the same variable. These 
        functions walk through the survey and sets the Question order.
        
        Note that a Branch's embedded data Questions are set before its 
        Pages' Questions. A Page's timer is set before its Questions.
        """
        print('setting order')
        var_count = {}
        self._set_order_branch(self.branch_stack[0], var_count)
    
    def _set_order_branch(self, branch, var_count):
        """Set the order for Questions belonging to a given Branch"""
        print('setting branch order', branch)
        [self._set_order_question(q, var_count) for q in branch.embedded]
        [self._set_order_page(p, var_count) for p in branch.pages]
        if branch.next_branch in self.branch_stack:
            self._set_order_branch(branch.next_branch, var_count)
    
    def _set_order_page(self, page, var_count):
        """Set the order for Questions belonging to a given Page"""
        print('setting page order', page)
        questions = page.questions_with_timer
        [self._set_order_question(q, var_count) for q in questions]
        if page.next_branch in self.branch_stack:
            self._set_order_branch(page.next_branch, var_count)
        
    def _set_order_question(self, question, var_count):
        """Set the order for a given Question"""
        print('setting question order', question)
        var = question.var
        if var is None:
            return
        if var not in var_count:
            var_count[var] = 0
        question.order = var_count[var]
        var_count[var] += 1