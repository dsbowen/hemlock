"""Participant database models

A `Participant` has the following primary responsibilities:
1. Navigation. A `Participant` contains a `branch_stack` and `_router` for 
navigation.
2. Data recording. Participants gather and store their data elements in the 
`DataStore`.

A participant may have one of three `status`es: InProgress, Completed, 
TimedOut. When a participant's status changes to Completed or TimedOut, a 
participant's data probably will not change, so it caches its data in the 
`DataStore`. (However, if a participant's status changes back to InProgress,
its data will be re-recorded.)

Participants also contain a mutable dictionary, `g`, as well as a dictonary 
of metadata, `meta`.
"""

from hemlock.app import db
from hemlock.database.bases import Base
from hemlock.database.private import DataStore, Router
from hemlock.database.types import DataFrame
from hemlock.tools import random_key

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
    _key = db.Column(db.String(90))
    _data_store_id = db.Column(db.Integer, db.ForeignKey('data_store.id'))

    _router = db.relationship('Router', backref='part', uselist=False)
    
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
    def data_elements(self):
        elements = [e for b in self.branch_stack for e in b.data_elements]
        elements.sort(key=lambda e: e.id)
        return elements
    
    _viewing_pages = db.relationship(
        'ViewingPage',
        backref='part',
        order_by='ViewingPage.index',
        collection_class=ordering_list('index')
    )

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
            return 'Completed'
        if self.time_expired:
            return 'TimedOut'
        return 'InProgress'
    
    @Base.init('Participant')
    def __init__(self, meta={}):
        """Initialize Participant"""
        super().__init__()
        
        ds = DataStore.query.first()
        ds.meta.append(meta)
        ds.update_status(self)
        db.session.commit()

        self._key = random_key()
        self.end_time = self.start_time = datetime.utcnow()
        self.meta = meta.copy()
        self.g = {}

    def update_end_time(self):
        self.end_time = datetime.utcnow()

    def _init_tree(self, root_f):
        """Initialize a new tree"""
        self._router = Router(root_f)
        self.current_branch = root = root_f()
        self.branch_stack.append(root)
        root.current_page = root.start_page
        root.is_root = True
        if not self.current_branch.pages:
            self._router.navigator.forward_recurse()
    
    """Data packaging"""
    @property
    def meta(self):
        self._meta['ID'] = self.id
        self._meta['EndTime'] = self.end_time
        self._meta['StartTime'] = self.start_time
        self._meta['Status'] = self.status
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
        self._set_order()
        elements = self.data_elements
        df = DataFrame()
        df.add(data=self.meta, all_rows=True)
        [df.add(data=e._pack_data(), all_rows=e.all_rows) for e in elements]
        df.pad()
        return df
    
    def _set_order(self):
        """Set the order for all data elements
        
        An element's order is the order in which it appeared to the 
        Participant relative to other elements of the same variable. These 
        functions walk through the survey and set the element order.
        
        Note that a Branch's embedded data elements are set before its 
        Pages' elements. A Page's Timer is set before its Questions.
        """
        var_count = {}
        if self.branch_stack:
            self._set_order_branch(self.branch_stack[0], var_count)
    
    def _set_order_branch(self, branch, var_count):
        """Set the order for Questions belonging to a given Branch"""
        [self._set_order_element(e, var_count) for e in branch.embedded]
        [self._set_order_page(p, var_count) for p in branch.pages]
        if branch.next_branch in self.branch_stack:
            self._set_order_branch(branch.next_branch, var_count)
    
    def _set_order_page(self, page, var_count):
        """Set the order for Questions belonging to a given Page"""
        elements = page.data_elements
        [self._set_order_element(e, var_count) for e in elements]
        if page.next_branch in self.branch_stack:
            self._set_order_branch(page.next_branch, var_count)
        
    def _set_order_element(self, element, var_count):
        """Set the order for a given data element"""
        var = element.var
        if var is None:
            return
        if var not in var_count:
            var_count[var] = 0
        element.order = var_count[var]
        var_count[var] += 1