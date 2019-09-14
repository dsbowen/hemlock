"""Question database model

Relationships:

branch: the branch to which this question belongs
page: the page to which this question belongs
choices: list of Choices (e.g. for single choice questions)
selected_choices: list of Choices the Participant selected
nonselected_choices: list of avaialble Choices the Participant did not select
validators: list of Validators (to validate Participant's response)

Public (non-Function) Columns:

all_rows: indicates this Question's data should appear in all dataframe rows 
    for its Participant
data: data this Question contributes to its variable
default: default response (Mutable object)
error: error message
init_default: initial default response. If changed, default can be reset to 
    its initial value with question.reset_default()
qtype: Question type (must have a registered html compiler)
text: Question text
var: name of the variable to which this Question contributes data

Function Columns:

compile: run before html is compiled
debug: run during debugging
post: run after data are recorded
"""

from hemlock.app import db
from hemlock.database.private import Base
from hemlock.database.types import Function, FunctionType

from bs4 import BeautifulSoup
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import Mutable, MutableType
from sqlalchemy_mutable import MutableListType, MutableDictType

REGISTRATIONS = ['html_compiler', 'response_recorder', 'data_recorder']


class Question(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    @property
    def qid(self):
        return 'q{}'.format(self.id)
    
    # _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    # _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _page_timer_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    index = db.Column(db.Integer)
    
    choices = db.relationship(
        'Choice', 
        backref='question',
        order_by='Choice.index',
        collection_class=ordering_list('index'),
        foreign_keys='Choice._question_id'
        )
    
    selected_choices = db.relationship(
        'Choice',
        order_by='Choice._selected_index',
        collection_class=ordering_list('_selected_index'),
        foreign_keys='Choice._selected_id'
        )
    
    nonselected_choices = db.relationship(
        'Choice',
        order_by='Choice._nonselected_index',
        collection_class=ordering_list('_nonselected_index'),
        foreign_keys='Choice._nonselected_id'
        )
        
    validators = db.relationship(
        'Validator', 
        backref='question', 
        order_by='Validator.index',
        collection_class=ordering_list('index')
        )
        
    all_rows = db.Column(db.Boolean)
    data = db.Column(db.PickleType)
    _default = db.Column(MutableType)
    error = db.Column(db.Text)
    init_default = db.Column(MutableType)
    _qtype = db.Column(db.String)
    text = db.Column(db.Text)
    var = db.Column(db.Text)
    
    compile = db.Column(FunctionType)
    debug = db.Column(FunctionType)
    post = db.Column(FunctionType)
    
    @property
    def default(self):
        return self._default
    
    @default.setter
    def default(self, default):
        """Set initial default the first time default is set"""
        if self.init_default is None:
            self.init_default = default
        self._default = default
    
    @property
    def qtype(self):
        return self._qtype
    
    @qtype.setter
    def qtype(self, qtype):
        assert qtype in self.html_compiler, (
            'Question type does not have an associated html compiler'
            )
        self._qtype = qtype
    
    """
    Register question types with html compilers, response recorders, and
    data recorders
    """
    html_compiler = {}
    response_recorder = {}
    data_recorder = {}

    @classmethod
    def register(cls, qtype, registration):
        assert registration in REGISTRATIONS
        def register(func):
            getattr(cls, registration)[qtype] = func
            return func
        return register
    
    def __init__(
            self, page=None, branch=None, index=None, 
            choices=[], validators=[],
            all_rows=False, data=None, default=Mutable(),
            qtype='text', text='', var=None,
            compile=Function(), post=Function(), debug=Function()):
        
        db.session.add(self)
        db.session.flush([self])
        
        self.set_branch(branch, index)
        self.set_page(page, index)
        self.choices = choices
        self.validators = validators
        
        self.all_rows = all_rows
        self.data = data
        self.default = default
        self.qtype = qtype
        self.text = text
        self.var = var
        
        self.compile = compile
        self.debug = debug
        self.post = post
    
    def set_branch(self, branch, index=None):
        self._set_parent(branch, index, 'branch', 'embedded')
        
    def set_page(self, page, index=None):
        self._set_parent(page, index, 'page', 'questions')
        
    def reset_default(self):
        self.default = self.init_default
    
    def _compile_html(self):
        return self.html_compiler[self.qtype](self)
    
    def view_html(self):
        """View compiled html for debugging purposes"""
        soup = BeautifulSoup(self._compile_html(), 'html.parser')
        print(soup.prettify())

    def _record_response(self, response):
        """Record Participant response"""
        response_recorder = self.response_recorder.get(self.qtype)
        if response_recorder is not None:
            return response_recorder(self, response)
        self.response = response
        
    def _validate_response(self):
        """Validate Participant response"""
        for v in self.validators:
            self.error = v.validate()
            if self.error is not None:
                return False
        return True
    
    def _record_data(self):
        """Record Question data"""
        data_recorder = self.data_recorder.get(self.qtype)
        if data_recorder is not None:
            return data_recorder(self)
        self.data = self.response
        
    # Output the data (both question data and order data)
    # data consists of:
    # main data (usually referred to simply as 'data')
    # page (or branch) order: order in which question appeared its page
    # variable order: order in which question appeared
    #   relative to other questions belonging to the same variable
    # choice order for each choice
    def _output_data(self):
        if self.var is None:
            return {}
    
        data = {
            self.var: self.data,
            self.var+'_porder': self.index,
            self.var+'_vorder': self.vorder}
            
        for c in self.choices:
            data['_'.join([self.var, c.label, 'qorder'])] = c.index
            
        return data