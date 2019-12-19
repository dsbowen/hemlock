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
from hemlock.database.private import Base

from sqlalchemy_mutable import MutableType, MutableModelBase


class Question(Base, MutableModelBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'polymorphic_on': type
    }

    """Page relationship"""
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    index = db.Column(db.Integer)

    """Data columns"""
    all_rows = db.Column(db.Boolean)
    data = db.Column(MutableType)
    order = db.Column(db.Integer)
    var = db.Column(db.Text)

    @Base.init('Question')
    def __init__(self):
        super().__init__()
        
    def _pack_data(self, data=None):
        """Pack data for storing in DataStore
        
        Note: `var`Index is the index of the object; its order within its
        Branch, Page, or Question. `var`Order is the order of the Question
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