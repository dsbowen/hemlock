"""Branch database model

Relationships:

part: Participant to whom this Branch belongs
origin_branch: Branch from which this Branch originated
next_branch: Branch originating from this Branch
origin_page: Page from which this Branch originated
pages: queue of Pages to be displayed
embedded: set of embedded data Questions

Functions:

navigate: creates the next Branch to which the experiment navigates
"""

from hemlock.app import db
from hemlock.database.private.base import BranchingBase
from hemlock.database.types import Function, FunctionType

from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list


class Branch(db.Model, BranchingBase):
    id = db.Column(db.Integer, primary_key=True)
    
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _part_head_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    index = db.Column(db.Integer)
    
    _origin_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    origin_branch = db.relationship(
        'Branch',
        back_populates='next_branch',
        uselist=False,
        foreign_keys='Branch._origin_branch_id'
        )
        
    _next_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    next_branch = db.relationship(
        'Branch',
        back_populates='origin_branch',
        uselist=False,
        remote_side=id,
        foreign_keys='Branch._next_branch_id'
        )
    
    _origin_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    origin_page = db.relationship(
        'Page', 
        back_populates='next_branch',
        foreign_keys='Branch._origin_page_id'
        )
    
    pages = db.relationship(
        'Page', 
        backref='branch', 
        order_by='Page.index',
        collection_class=ordering_list('index'),
        foreign_keys='Page._branch_id'
        )
    
    @property
    def start_page(self):
        """Return the start of the page queue"""
        return self.pages[0] if self.pages else None
        
    current_page = db.relationship(
        'Page', 
        uselist=False,
        foreign_keys='Page._branch_head_id'
        )
        
    embedded = db.relationship(
        'Question', 
        backref='branch',
        order_by='Question.index',
        collection_class=ordering_list('index')
        )
        
    @property
    def questions(self):
        page_questions = [
            q for p in self.pages for q in p.questions+[p.timer]]
        return page_questions + self.embedded
        
    navigate = db.Column(FunctionType)
    _isroot = db.Column(db.Boolean)

    def __init__(self, pages=[], embedded=[], navigate=None):
        BranchingBase.__init__(self)
        
        self.pages = pages
        self.embedded = embedded
        self.navigate = navigate
        self._isroot = False
        
    def _forward(self):
        """Advance forward to the next page in the queue"""
        if self.current_page is None:
            return
        new_head_index = self.current_page.index + 1
        if new_head_index == len(self.pages):
            self.current_page = None
            return
        self.current_page = self.pages[new_head_index]
    
    def _back(self):
        """Return to previous page in queue"""
        if not self.pages:
            return
        if self.current_page is None:
            self.current_page = self.pages[-1]
            return
        new_head_index = self.current_page.index - 1
        self.current_page = self.pages[new_head_index]
        
    def view_nav(self):
        """Print page queue for debugging purposes"""
        INDENT = '    '
        HEAD_PART = '<== head branch of participant'
        HEAD_BRANCH = '<== head page of branch'
        indent = INDENT*(0 if self.index is None else self.index)
        head_part = HEAD_PART if self == self.part.current_branch else ''
        print(indent, self, head_part)
        [p.view_nav(indent) for p in self.pages]
        head_branch = HEAD_BRANCH if None == self.current_page else ''
        print(indent, None, head_branch)
        if self.next_branch in self.part.branch_stack:
            self.next_branch.view_nav()