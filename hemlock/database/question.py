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
"""

from hemlock.app import db
from hemlock.database.private import CompileBase, FunctionBase

from flask import current_app
from flask_login import current_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import Mutable, MutableType, MutableModelBase, MutableListType


class Question(MutableModelBase, CompileBase, FunctionBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'polymorphic_on': type
    }
    
    """Relationships to primary models"""
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _page_timer_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    index = db.Column(db.Integer)
    
    choice_div_classes = db.Column(MutableListType)
    choice_input_type = db.Column(db.String(50))
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
    
    """Relationships to function models"""
    compile_functions = db.relationship(
        'Compile',
        backref='question',
        order_by='Compile.index',
        collection_class=ordering_list('index')
    )

    validate_functions = db.relationship(
        'Validate', 
        backref='question', 
        order_by='Validate.index',
        collection_class=ordering_list('index')
    )
    
    submit_functions = db.relationship(
        'Submit',
        backref='question',
        order_by='Submit.index',
        collection_class=ordering_list('index')
    )
    
    """Columns"""
    all_rows = db.Column(db.Boolean)
    data = db.Column(MutableType)
    default = db.Column(MutableType)
    div_classes = db.Column(MutableListType)
    error = db.Column(db.Text)
    order = db.Column(db.Integer)
    response = db.Column(MutableType)
    text = db.Column(db.Text)
    var = db.Column(db.Text)
    
    def __init__(
            self, page=None, index=None,
            choice_div_classes=[], choice_input_type=None, choices=[],
            compile_functions=[], validate_functions=[], submit_functions=[],
            all_rows=False, data=None, default=None, div_classes=[], 
            text=None, var=None
        ):
        self.set_page(page, index)
        self.choice_div_classes = choice_div_classes
        self.choice_input_type = choice_input_type
        self.choices = choices

        self._set_function_relationships()
        self.compile_functions = compile_functions
        self.validate_functions = validate_functions
        self.submit_functions = submit_functions
        
        self.all_rows = all_rows
        self.data = data
        self.default = default
        self.div_classes = div_classes
        self.text = text
        self.var = var
        
        super().__init__(current_app.question_settings)
    
    """API methods"""
    def set_page(self, page, index=None):
        self._set_parent(page, index, 'page', 'questions')
    
    """Methods executed during study"""
    def _compile(self, content=''):
        """HTML compiler"""
        div_classes = self._compile_div_classes()
        label = self._compile_label()
        return DIV.format(
            id=self.model_id, classes=div_classes, 
            label=label, content=content
        )
    
    def _compile_div_classes(self):
        """Get question <div> classes
        
        Add the error class if the response was invalid.
        """
        div_classes = ' '.join(self.div_classes)
        if self.error is not None:
            return div_classes + ' error'
        return div_classes
    
    def _compile_label(self):
        """Get the question label"""
        error = self.error
        error = '' if error is None else ERROR.format(error=error)
        text = self.text if self.text is not None else ''
        return LABEL.format(id=self.model_id, text=error+text)

    def _record_response(self, response):
        return
        
    def _validate(self):
        """Validate Participant response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        for validate_function in self.validate_functions:
            self.error = validate_function()
            if self.error is not None:
                return False
        return True
    
    def _submit(self):
        """Submit response

        The question submit method will usually be used for data recording.
        """
        self.data = self.response
        
    def _pack_data(self, data=None):
        """Pack data for storing in DataStore
        
        Note: <var>Index is the index of the object; its order within its
        Branch, Page, or Question. <var>Order is the order of the Question
        relative to other Questions with the same variable.
        
        The optional `data` argument is prepacked data from the question 
        polymorph.
        """
        if self.var is None:
            return {}
        data = {self.var: self.data} if data is None else data
        if not self.all_rows:
            data[self.var+'Order'] = self.order
        if self.index is not None:
            data[self.var+'Index'] = self.index
        for c in self.choices:
            if c.label is not None:
                data[''.join([self.var, c.label, 'Index'])] = c.index
        return data

DIV = """
<div id="{id}" class="{classes}">
    {label}
    {content}
</div>
"""

ERROR = """
<span style="color:red">
    {error}
</span>
"""

LABEL = """
<label class="w-100" for="{id}">
    {text}
</label>
"""