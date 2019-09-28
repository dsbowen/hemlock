"""Question database model

Each Question executes 6 tasks:

1. Compile function: The Question executes a function immediately before its 
html is compiled.
2. Compile html: The Question compiles html for the client. This html will 
be inserted into its Page's html when the Participant accesses it, along 
with the html from other Questions on that Page.
3. Record response: The Question records the Participant's response.
4. Validate response: The Question checks whether the Participant's response 
was valid by checking with each of its Validators.
5. Record data: Having received a valid response, the Question records its 
data. This is usually the raw response or a transformation thereof.
6. Pack data: The Question packages its data for insertion into the 
DataStore.

Relationships:

branch: the branch to which this question belongs
nav: navigation bar
page: the page to which this question belongs
choices: list of Choices (e.g. for single choice questions)
selected_choices: list of Choices the Participant selected
nonselected_choices: list of available Choices the Participant did not select
validators: list of Validators (to validate Participant's response)

Public (non-Function) Columns:

all_rows: indicates this Question's data should appear in all dataframe rows 
    for its Participant
data: data this Question contributes to its variable
default: default response (Mutable object)
error: error message
init_default: initial default response. If changed, default can be reset to 
    its initial value with question.reset_default()
text: Question text
var: name of the variable to which this Question contributes data

Function Columns:

compile: run before html is compiled
debug: run during debugging
post: run after data are recorded
"""

from hemlock.app import db
from hemlock.database.private import CompileBase
from hemlock.database.types import FunctionType

from flask import current_app
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import Mutable, MutableType, MutableModelBase, MutableListType, MutableDictType


class Question(MutableModelBase, CompileBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'polymorphic_on': type
        }
    
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
    data = db.Column(MutableType)
    _default = db.Column(MutableType)
    error = db.Column(db.Text)
    init_default = db.Column(MutableType)
    order = db.Column(db.Integer)
    response = db.Column(MutableType)
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
    
    def __init__(
            self, page=None, index=None, choices=[], validators=[],
            all_rows=False, data=None, default=None, text=None, var=None,
            compile=None, debug=None, post=None):
        self.set_page(page, index)
        self.choices = choices
        self.validators = validators
        
        self.all_rows = all_rows
        self.data = data
        self.default = default
        self.text = text
        self.var = var
        
        self.compile = compile or current_app.question_compile
        self.debug = debug or current_app.question_debug
        self.post = post or current_app.question_post
        
        super().__init__()
    
    """API methods"""
    def set_page(self, page, index=None):
        self._set_parent(page, index, 'page', 'questions')
        
    def reset_default(self):
        self.default = self.init_default
    
    """Methods executed during study"""
    def compile_html(self):
        """
        Question types are responsible for implementing their own html 
        compiler.
        """
        raise NotImplementedError('Question must have a compile_html method')

    def record_response(self, response):
        self.response = response
        
    def validate(self):
        """Validate Participant response
        
        Keep the error message associated with the first failed Validator.
        """
        for v in self.validators:
            self.error = v.validate(object=self)
            if self.error is not None:
                return False
        return True
    
    def record_data(self):
        self.data = self.response
        
    def pack_data(self, data=None):
        """Pack data for storing in DataStore
        
        Note: <var>Index is the index of the object; its order within its
        Branch, Page, or Question. <var>Order is the order of the Question
        relative to other Questions with the same variable.
        
        The optional `data` argument is prepacked data from the question type.
        """
        if self.var is None:
            return {}
        data = {self.var: self.data} if data is None else data
        if not self.all_rows:
            data[self.var+'Order'] = self.order
        if self.index is not None:
            data[self.var+'Index'] = self.index
        for c in self.choices:
            data[''.join([self.var, c.label, 'Index'])] = c.index
        return data