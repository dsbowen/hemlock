##############################################################################
# Question model
# by Dillon Bowen
# last modified 09/08/2019
##############################################################################

from hemlock.factory import attr_settor, compiler, db
from .choice import Choice
from hemlock.models.private.base import Base, iscallable
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_json import NestedMutableJson

# from sqlalchemy_json import NestedMutable
# class NestedMutablePickle(db.PickleType):
    # pass
    
# NestedMutable.associate_with(NestedMutablePickle)

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
        collection_class=ordering_list('index')
        )
        
    validators = db.relationship(
        'Validator', 
        backref='question', 
        order_by='Validator.index',
        collection_class=ordering_list('index')
        )
        
    text = db.Column(db.Text)
    all_rows = db.Column(db.Boolean)
    qtype = db.Column(db.String)
    var = db.Column(db.Text)
    
    default = db.Column(db.PickleType)
    init_default = db.Column(db.PickleType)
    _default_is_choice = db.Column(db.Boolean)
    
    compile = db.Column(db.PickleType)
    compile_args = db.Column(db.PickleType)
    post = db.Column(db.PickleType)
    post_args = db.Column(NestedMutableJson)
    debug = db.Column(db.PickleType)
    debug_args = db.Column(db.PickleType)
    
    data = db.Column(db.PickleType)
    response = db.Column(db.Text)
    error = db.Column(db.Text)
    vorder = db.Column(db.Integer)
    
    # Initialize question
    def __init__(
            self, page=None, branch=None, index=None,
            text='',  all_rows=False, default=None, qtype='text', var=None,
            compile=None, compile_args={},
            post=None, post_args={},
            debug=None, debug_args={},
            data=None):
        
        db.session.add(self)
        db.session.flush([self])
        
        self.set_branch(branch, index)
        self.set_page(page, index)
        
        self.text = text
        self.all_rows = all_rows
        self.default = default
        self.qtype = qtype
        self.var = var
        
        self.compile, self.compile_args = compile, compile_args
        self.post, self.post_args = post, post_args
        self.debug, self.debug_args = debug, debug_args
        
        self.data = data
    
    
    
    ##########################################################################
    # Public methods
    ##########################################################################
    
    # Set branch
    def set_branch(self, branch, index=None):
        self._set_parent(branch, index, 'branch', 'embedded')
        
    # Set page
    def set_page(self, page, index=None):
        self._set_parent(page, index, 'page', 'questions')
        
    # Reset default to initial default
    # typically for use after invalid page submission
    def reset_default(self):
        self.default = self.init_default
        
    # Get the list of selected choices
    def get_selected(self):
        return [c for c in self.choices if c._checked=='checked']
        
    # Get the list of nonselected choices
    def get_nonselected(self):
        return [c for c in self.choices if c._checked=='']
    
        
    
    ##########################################################################
    # Private methods
    ##########################################################################
        
    # Record the participant's response
    # collect response and update default
    def _record_response(self, response):
        # if self._qtype == 'free':
            # self._default = response
        # else:
            # [c._set_checked(response=='c'+str(c.id)) for c in self._choices]
            # checked = self.get_selected()
            # if checked:
                # response = checked[0].get_value()
                # self._default = checked[0].id
        self.response = self.data = response
        
    # Validate the participant's response
    def _validate(self):
        for v in self.validators:
            self.error = v._get_error()
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
        
# Question may be assigned to page or branch but not both
@attr_settor.register(Question, 'page')
def remove_from_branch(question, value):
    from hemlock.models.page import Page
    if isinstance(value, Page):
        question.branch = None
    return value

@attr_settor.register(Question, 'branch')
def remove_from_page(question, value):
    from hemlock.models.branch import Branch
    if isinstance(value, Branch):
        question.page = None
    return value
        
# Validate function attributes are callable (or None)
@attr_settor.register(Question, ['compile', 'post', 'debug'])
def valid_function(question, value):
    return iscallable(value)
    
# Validate question type exists
@attr_settor.register(Question, 'qtype')
def valid_qtype(question, value):
    if value not in compiler.compile_functions:
        raise ValueError('Nonexistent question type')
    return value
    
# Set initial default value if not already set
@attr_settor.register(Question, 'default')
def init_default(question, value):
    if question.init_default is None:
        question.init_default = value
    return value