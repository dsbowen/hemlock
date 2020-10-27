"""# Participant"""

from ..app import db, settings
from ..tools import key
from .bases import Base
from .private import DataFrame, DataStore, Router

from flask_login import UserMixin, login_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import MutableDictType

from datetime import datetime
from random import randint

settings['Participant'] = {'g': {}, 'meta': {}}

def _send_data(func):
    """Send data to the DataStore
    
    Begin by recording the Participant's previous status. If the status has
    changed as a result of the update, register the change in the `DataStore`.
    """
    def status_update(part, update):
        part._previous_status = part.status
        return_val = func(part, update)
        if part._previous_status == part.status:
            return return_val
        DataStore.query.first().update_status(part)
        return return_val
    return status_update


class Participant(UserMixin, Base, db.Model):
    """
    The Participant class stores data for an individual survey participant and
    handles navigation for that participant.

    Inherits from [`hemlock.models.Base`](bases.md).

    Attributes
    ----------
    completed : bool, default=False
        Indicates that the participant has completed the survey.

    end_time : datetime.datetime
        Last time the participant submitted a page.

    g : dict, default={}
        Dictionary of miscellaneous objects.

    meta : dict, default={}
        Participant metadata, such as IP address.

    start_time : datetime.datetime
        Time at which the participant started he survey.

    status : str, default='InProgress'
        Participant's current status; `'InProgress'`, `'TimedOut'`, or 
        `'Completed'`. Read only; derived from `self.completed` and 
        `self.time_expired`.

    time_expired : bool, default=False
        Indicates that the participant has exceeded their allotted time for 
        the survey.

    updated : bool, default=True
        Indicates that the participant's data was updated after the last time 
        their data was stored; if `True`, the participant's data will be 
        re-stored when data are downloaded.

    Relationships
    -------------
    branch_stack : list of hemlock.Branch
        The participant's stack of branches.

    current_branch : hemlock.Branch
        Participant's current branch (head of `self.branch_stack`).

    current_page : hemlock.Page
        Participant's current page (head of `self.current_branch`).

    pages : list of hemlock.Page
        Pages belonging to the participant.

    embedded : list of hemlock.Embedded
        Embedded data elements belonging to the participant.

    data_elements : list of hemlock.DataElement
        List of all data elements belonging to the participant, ordered by 
        `id`.

    Examples
    --------
    ```python
    from hemlock import Branch, Label, Page, Participant, push_app_context

    def start():
    \    return Branch(Page(Label('<p>Hello World</p>')))

    app = push_app_context()

    part = Participant.gen_test_participant(start)
    part.current_page.preview()
    ```
    """
    id = db.Column(db.Integer, primary_key=True)
    _key = db.Column(db.String(90))
    _data_store_id = db.Column(db.Integer, db.ForeignKey('data_store.id'))

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

    embedded = db.relationship(
        'Embedded',
        backref='part',
        order_by='Embedded.index',
        collection_class=ordering_list('index'),
    )
        
    @property
    def data_elements(self):
        elements = [e for e in self.embedded]
        elements += [e for b in self.branch_stack for e in b.data_elements]
        elements.sort(key=lambda e: e.id)
        return elements
    
    _viewing_pages = db.relationship(
        'ViewingPage',
        backref='part',
        order_by='ViewingPage.index',
        collection_class=ordering_list('index')
    )

    _previous_status = db.Column(db.String(16))
    _completed = db.Column(db.Boolean, default=False)
    end_time = db.Column(db.DateTime)
    g = db.Column(MutableDictType)
    meta = db.Column(MutableDictType)
    start_time = db.Column(db.DateTime)
    _time_expired = db.Column(db.Boolean, default=False)
    updated = db.Column(db.Boolean, default=True)
    
    @property
    def completed(self):
        return self._completed
        
    @completed.setter
    @_send_data
    def completed(self, completed):
        self._completed = completed
        
    @property
    def time_expired(self):
        return self._time_expired
        
    @time_expired.setter
    @_send_data
    def time_expired(self, time_expired):
        self._time_expired = time_expired
    
    @property
    def status(self):
        if self.completed:
            return 'Completed'
        if self.time_expired:
            return 'TimedOut'
        return 'InProgress'
    
    def __init__(self, **kwargs):
        self._key = key()
        self.end_time = self.start_time = datetime.utcnow()
        super().__init__(**kwargs)

        ds = DataStore.query.first()
        ds.meta.append(self.meta)
        if not settings.get('collect_IP'):
            self.meta.pop('IPv4', None)
        ds.update_status(self)

    def _init_tree(self, gen_root):
        """
        Initialize a new tree.
        
        Parameters
        ----------
        gen_root : callable
            Generates the root branch of the tree.

        Returns
        -------
        self
        """
        self._router = Router(gen_root)
        self.current_branch = root = gen_root()
        self.branch_stack.append(root)
        root.current_page = root.start_page
        if not self.current_branch.pages:
            self._router.navigator.forward_recurse()
        return self

    def back(self, back_to=None):
        """
        Navigate back for debugging purposes.

        Parameters
        ----------
        back_to : hemlock.Page or None, default=None
            Navigate back to this page; if `None`, navigate back one page.

        Returns
        -------
        self : hemlock.Participant
        """
        self._router.navigator.back(back_to)
        return self

    def forward(self, forward_to=None):
        """
        Navigate forward for debugging purposes.

        Parameters
        ----------
        forward_to : hemlock.Page or None, default=None
            Navigate forward to this page; if `None`, navigate forward one 
            page.

        Returns
        -------
        self : hemlock.Participant
        """
        self._router.navigator.forward(forward_to)
        return self

    def gen_test_participant(gen_root=None):
        """
        Generate a test participant for debugging purposes.

        Parameters
        ----------
        gen_root : callable or None, default=None
            Function to generate the root branch of the participant's tree.
            This should return a `hemlock.Branch`.

        Returns
        -------
        part : hemlock.Participant
        """
        part = Participant(meta={})
        login_user(part)
        if gen_root:
            part._init_tree(gen_root)
        return part

    def get_data(self):
        """
        Returns
        -------
        df : hemlock.models.private.DataFrame
            Data associated with the participant.

        Examples
        --------

        Notes
        -----
        Data elements are added to the dataframe in the order in which they 
        were created (i.e. by id). This is not necessarily the order in which 
        they appeared to the Participant.
        """
        self._set_order()
        elements = self.data_elements
        df = DataFrame()
        df.add(data=self.get_meta(), rows=-1)
        [df.add(data=e._pack_data(), rows=e.data_rows) for e in elements]
        df.pad()
        return df
    
    def _set_order(self):
        """Set the order for all data elements
        
        An element's order is the order in which it appeared to the 
        Participant relative to other elements of the same variable. These 
        functions walk through the survey and set the element order.
        
        The participant's embedded data are set first, followed by its
        branches' data. A branch's embedded data are set first, followed by
        its page's data. A page's embedded data are set first, followed by its
        timer, followed by its quesitons.
        """
        var_count = {}
        [self._set_order_element(e, var_count) for e in self.embedded]
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
    
    def get_meta(self):
        """
        This is where it gets meta.

        Returns
        -------
        meta : dict
            Participant's metadata, including the ID, end time, start time, 
            and current status.
        """
        meta = self.meta.copy()
        meta.update({
            'ID': self.id,
            'EndTime': self.end_time,
            'StartTime': self.start_time,
            'Status': self.status
        })
        return meta

    def view_nav(self):
        """
        View participant's branch stack.

        Returns
        -------
        self : hemlock.Participant
        """
        self.branch_stack[0].view_nav()
        print('\n C = current page \n T = terminal page\n')
        return self