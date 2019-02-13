###############################################################################
# Question model
# by Dillon Bowen
# last modified 02/12/2019
###############################################################################

from hemlock import db
from hemlock.models.choice import Choice
from hemlock.models.validator import Validator
from hemlock.models.base import Base
from sqlalchemy import and_

# Renders errors from previous submit
def render_error(q):
    if q._error is None:
        return ''
    return '''
        <div style='color: #ff0000;'>
        {0}
        </div>
        '''.format(q._error)

# Renders question text in html format
def render_text(q):
    return '''
        {0}
        <br></br>
        '''.format(q._text)
        
# Renders the question body in html format
def render_body(q):
    if q._qtype == 'text':
        return ''
    if q._qtype == 'free':
        return render_free(q)
    if q._qtype == 'single choice':
        return render_single_choice(q)
    
# Renders free response question in html format
def render_free(q):
    return '''
        <input name='{0}' type='text' value=''>
        '''.format(q.id)
    
# Renders single choice question in html format
def render_single_choice(q):
    choices = q._choices.order_by('_order').all()
    choice_html = ['''
        <input name='{0}' type='radio' value='{1}'>{2}
        <br></br>
        '''.format(q.id, c._value, c._text) for c in choices]
    return ''.join(choice_html)

'''
Data:
_part_id: ID of participant to whom question belongs
_branch_id: ID of branch to which question belongs (embedded questions only)
_page_id: ID of page to which question belongs
_choices: list of choices (e.g. for single choice questions
_validators: list of validators
_order: order in which the question appears on the page
_text: question text
_qtype: question type
_var: variable to which the question contributes data
_all_rows: indicates that question data appears on all rows
_render_function: function called before redering the page
_render_args: arguments for the render function
_post_function: function called after responses are submitted and validated
_post_args: arguments for the post function
_randomize: indicator of choice randomization
_default: default option or entry
_rendered: indicator that the question was previously rendered
_error: stores an error message if response was invalid
_entry: participant's raw data entry
_data: response data (cleaned version of entry)
_vorder: order in which this question appears in its variable
'''
class Question(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _choices = db.relationship('Choice', backref='_question', lazy='dynamic')
    _validators = db.relationship('Validator', backref='_question', lazy='dynamic')
    _order = db.Column(db.Integer)
    _text = db.Column(db.Text)
    _qtype = db.Column(db.String(16))
    _var = db.Column(db.Text)
    _all_rows = db.Column(db.Boolean)
    _render_function = db.Column(db.PickleType)
    _render_args = db.Column(db.PickleType)
    _post_function = db.Column(db.PickleType)
    _post_args = db.Column(db.PickleType)
    _randomize = db.Column(db.Boolean)
    _default = db.Column(db.Text)
    _rendered = db.Column(db.Boolean, default=False)
    _error = db.Column(db.PickleType)
    _entry = db.Column(db.Text)
    _data = db.Column(db.PickleType)
    _vorder = db.Column(db.Integer)
    
    # Adds question to database and commits on initialization
    def __init__(self, branch=None, page=None, order=None, text='', 
        qtype='text', var=None, all_rows=False,
        render=None, render_args=None,
        post=None, post_args=None,
        randomize=False, default=None, data=None):
        
        self.assign_branch(branch)
        self.assign_page(page, order)
        self.set_text(text)
        self.set_qtype(qtype)
        self.set_var(var)
        self.set_all_rows(all_rows)
        self.set_render(render, render_args)
        self.set_post(post, post_args)
        self.set_randomize(randomize)
        self.set_default(default)
        self.set_data(data)
        
        db.session.add(self)
        db.session.commit()
        
    # Assign to branch
    def assign_branch(self, branch):
        if branch is not None:
            self._assign_parent('_branch', branch, branch._embedded.all())
            
    # Remove from branch
    def remove_branch(self):
        if self._branch is not None:
            self._remove_parent('_branch', self._branch._embedded.all())
    
    # Assign to page
    def assign_page(self, page, order=None):
        if page is not None:
            self._assign_parent('_page', page, page._questions.all(), order)
            
    # Remove from page
    def remove_page(self):
        if self._page is not None:
            self._remove_parent('_page', self._page._questions.all())
            
    # Sets the question text
    def set_text(self, text):
        self._set_text(text)
        
    # Set question type
    def set_qtype(self, qtype):
        self._qtype = qtype
        
    # Set the variable in which question data will be stored
    def set_var(self, var):
        self._set_var(var)
        
    # Set the all_rows indicator
    # i.e. the data will appear in all of the participant's dataframe rows
    def set_all_rows(self, all_rows=True):
        self._set_all_rows(all_rows)
        
    # Set the render function and arguments
    def set_render(self, render=None, args=None):
        self._set_function('_render_function', render, '_render_args', args)
        
    # Set the post function and arguments
    def set_post(self, post=None, args=None):
        self._set_function('_post_function', post, '_post_args', args)
        
    # Turn randomization on/off (True/False)
    def set_randomize(self, randomize=True):
        self._set_randomize(randomize)
    
    # Set default answer
    def set_default(self, default):
        self._default = default
        
    # Set question data
    def set_data(self, data):
        self._data = data
        
    # Get question data
    def get_data(self):
        return self._data
        
    # Get question entry
    def get_entry(self):
        return self._entry
        
    # Get the list of selected choices
    def get_selected(self):
        return [c for c in self._choices if c._selected]
        
    # Get the list of nonselected choices
    def get_nonselected(self):
        return [c for c in self._choices if not c._selected]
        
    # Record the participant's entry
    def _record_entry(self, entry):
        self._entry = entry
        self.set_data(entry)
        if self._qtype == 'single choice':
            [c.set_selected() for c in self._choices if entry==str(c._value)]
        
    # Render the question in html
    def _render_html(self, part_id):
        self._first_render(self._choices.all())
        
        if self._qtype == 'embedded':
            html = ''
        else:
            html = '''
        <p>
            {0}
            {1}
            {2}
        </p>
        '''.format(render_error(self), render_text(self), render_body(self))
        
        self._rendered = True
        return html
        
    # Set the variable order
    def _set_vorder(self):
        if not self._var:
            return
        prev = Question.query.filter_by(_part_id=self._part_id, _var=self._var)
        self._vorder = len(prev.all())
        
    # Validate the participant's response
    def _validate(self):
        for v in self._validators:
            self._error = v._get_error()
            if self._error is not None:
                return False
        return True
        
    # Outputs the data (both question data and order data)
    def _output_data(self):
        # data, page order, and question order
        data = {
            self._var: self._data,
            self._var+'_porder': self._order,
            self._var+'_vorder': self._vorder}
            
        # choice order
        for c in self._choices:
            data['_'.join([self._var,c._label,'qorder'])] = c._order
            
        return data