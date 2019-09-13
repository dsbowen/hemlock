"""Question database model

A Branch may contain a list of Questions. These Questions do not appear in 
the survey, but contribute to the Participant's data in the DataStore.

A Page contains a list of Questions which appear on the survey page.

Questions of certain types (such as multiple choice) contain a list of 
Choices. Questions may also contain a list of Validators.
"""

from hemlock.factory import db
from hemlock.database_types import FunctionType
from hemlock.models.private.base import Base

from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import Mutable, MutableType
from sqlalchemy_mutable import MutableListType, MutableDictType


'''
Relationships:
    part: participant to whom this question belongs
    branch: branch to which this question belongs (embedded data)
    page: page to which this question belongs
    choices: list of choices
    validators: list of validators
    
NOTE: question may be assigned to page or branch but not both
    
Columns:
    text: question text
    all_rows: indicates that question data should appear in all rows
    qtype: question type
    var: variable to which this question belongs
    
    default: initial default option or participant's response from last post
    init_default: initial default option
    default_is_choice: indicates that default option type is Choice
    
    compile: function called when page html is compiled
    compile_args: arguments for compile function
    post: function called after page is submitted (posted)
    post_args: arguments for post function
    debug: debug function called by AI Participant
    debug_args: arguments for debug function
    
    data: question data
    response: participant's raw response
    error: error message for invalid participant response
    vorder: order in which question appeared relative to other questions
        belonging to the same variable
'''
class Question(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
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
    init_default = db.Column(MutableType)
    _qtype = db.Column(db.String)
    text = db.Column(db.Text)
    var = db.Column(db.Text)
    
    compile = db.Column(FunctionType)
    compile_args = db.Column(MutableListType)
    compile_kwargs = db.Column(MutableDictType)
    post = db.Column(FunctionType)
    post_args = db.Column(MutableListType)
    post_kwargs = db.Column(MutableDictType)
    debug = db.Column(FunctionType)
    debug_args = db.Column(MutableListType)
    debug_kwargs = db.Column(MutableDictType)
    
    response = db.Column(db.PickleType)
    error = db.Column(db.Text)
    
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
        assert qtype in self._html_compilers, (
            'Question type does not have an associated html compiler'
            )
        self._qtype = qtype
    
    """Associate question types with html compilers and response recorders"""
    _html_compilers = {}
    
    @classmethod
    def register_html_compiler(cls, qtype):
        def register(compiler):
            cls._html_compilers[qtype] = compiler
            return compiler
        return register
    
    _response_recorders = {}
    
    @classmethod
    def register_response_recorder(cls, qtype):
        def register(recorder):
            cls._response_recorders[qtype] = recorder
            return recorder
        return register
    
    def __init__(
            self, page=None, branch=None, index=None,
            all_rows=False, data=None, default=Mutable(),
            qtype='text', text='', var=None,
            compile=None, compile_args=[], compile_kwargs={},
            post=None, post_args=[], post_kwargs={},
            debug=None, debug_args=[], debug_kwargs={}):
        
        db.session.add(self)
        db.session.flush([self])
        
        self.set_branch(branch, index)
        self.set_page(page, index)
        
        self.all_rows = all_rows
        self.data = data
        self.default = default
        self.qtype = qtype
        self.text = text
        self.var = var
        
        self.compile = compile
        self.compile_args = compile_args
        self.compile_kwargs = compile_kwargs
        self.post = post
        self.post_args = post_args
        self.post_kwargs = post_kwargs
        self.debug = debug
        self.debug_args = debug_args
        self.debug_kwargs = debug_kwargs
    
    def set_branch(self, branch, index=None):
        self._set_parent(branch, index, 'branch', 'embedded')
        
    def set_page(self, page, index=None):
        self._set_parent(page, index, 'page', 'questions')
        
    def reset_default(self):
        self.default = self.init_default
    
    def _compile_html(self):
        return self._html_compilers[self.qtype](self)

    def _record_response(self, response):
        """Record Participant response
        
        Use a response recorder specific to the question type if one has been
        registered. Otherwise set data and response to Participant's response.
        """
        response_recorder = self._response_recorders.get(self.qtype)
        if response_recorder is not None:
            return response_recorder(self, response)
        self.data = self.response = response
        
    def _validate_response(self):
        """Validate Participant response"""
        for v in self.validators:
            self.error = v._validate()
            if self.error is not None:
                return False
        return True
        
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