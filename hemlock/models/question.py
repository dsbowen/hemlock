##############################################################################
# Question model
# by Dillon Bowen
# last modified 08/14/2019
##############################################################################

from hemlock.factory import db
from hemlock.models.choice import Choice
from hemlock.models.private.base import Base
from flask_login import current_user



'''
Relationships:
    part: participant to whom this question belongs
    branch: branch to which this question belongs (embedded data)
    page: page to which this question belongs
    choices: list of choices
    validators: list of validators
    
NOTE: a question may be assigned to a branch or page but not both
    
Columns:
    text: question text
    
    all_rows: indicates that question data should appear in all rows
    qtype: question type
    var: variable to which this question belongs
    
    default: initial default option or participant's response from last post
    init_default: initial default option
    default_is_choice: indicates that default option type is Choice
    
    compile_function: function called when page html is compiled
    compile_args: arguments for compile function
    post_function: function called after page is submitted (posted)
    post_args: arguments for post function
    debug_function: debug function called by AI Participant
    debug_args: arguments for debug function
    debug_attrs: attributes for Debug Question
    
    data: question data
    response: participant's raw response
    error: error message for invalid participant response
    vorder: order in which question appeared relative to other questions
        belonging to the same variable
'''
class Question(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _part_index = db.Column(db.Integer)
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _page_timer_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _index = db.Column(db.Integer)
    
    _choices = db.relationship(
        'Choice', 
        backref='_question', 
        lazy='dynamic',
        order_by='Choice._index')
        
    _validators = db.relationship(
        'Validator', 
        backref='_question', 
        lazy='dynamic',
        order_by='Validator._index')
        
    _text = db.Column(db.Text)
    
    _all_rows = db.Column(db.Boolean)
    _qtype = db.Column(db.String(16))
    _var = db.Column(db.Text)
    
    _default = db.Column(db.PickleType)
    _init_default = db.Column(db.PickleType)
    _default_is_choice = db.Column(db.Boolean)
    
    _compile_function = db.Column(db.PickleType)
    _compile_args = db.Column(db.PickleType)
    _post_function = db.Column(db.PickleType)
    _post_args = db.Column(db.PickleType)
    _debug_function = db.Column(db.PickleType)
    _debug_args = db.Column(db.PickleType)
    _debug_attrs = db.Column(db.PickleType)
    
    _data = db.Column(db.PickleType)
    _response = db.Column(db.Text)
    _error = db.Column(db.PickleType)
    _vorder = db.Column(db.Integer)
    
    
    
    # Initialize question
    def __init__(
            self, page=None, text='', part=None, branch=None, index=None,
            all_rows=False, default=None, qtype='text', var=None,
            compile=None, compile_args=None,
            post=None, post_args=None,
            debug=None, debug_args=None, debug_attrs=None,
            data=None):
        
        db.session.add(self)
        db.session.commit()
        
        self.participant(part)
        if branch is not None:
            self.branch(branch, index)
        if page is not None:
            self.page(page, index)
        
        self.text(text)
        
        self.all_rows(all_rows)
        self.default(default)
        self.qtype(qtype)
        self.var(var)
        
        self.compile(compile, compile_args)
        self.post(post, post_args)
        self.debug(debug, debug_args, debug_attrs)
        
        self.data(data)
    
    
    
    ##########################################################################
    # Manage parents
    ##########################################################################
    
    # PARTICIPANT
    # Assign to participant
    def participant(self, participant=current_user):
        self._assign_parent(participant, '_part')
        
    # Get participant
    def get_participant(self):
        return self._part
        
    # Remove from participant
    def remove_participant(self):
        self._remove_parent('_part')
        
    
    # BRANCH
    # Assign to branch
    # remove from page first
    def branch(self, branch, index=None):
        self.remove_page()
        self._assign_parent(branch, '_branch', index)
        if branch is not None:
            self.participant(branch._part)
        
    # Get branch
    def get_branch(self):
        return self._branch
            
    # Remove from branch
    def remove_branch(self):
        self._remove_parent('_branch')
        self.remove_participant()
        
        
    # PAGE
    # Assign to page and page's participant
    # remove from branch first
    def page(self, page, index=None):
        self.remove_branch()
        self._assign_parent(page, '_page', index)
        if page is not None:
            self.participant(page._part)
        
    # Get page
    def get_page(self):
        return self._page
        
    # Get position within page (or less commonly, within branch)
    def get_index(self):
        return self._index
        
    # Remove from page
    def remove_page(self):
        self._remove_parent('_page')
        self.remove_participant()
    
    
    
    ##########################################################################
    # Manage children
    ##########################################################################
    
    # CHOICES
    # Get list of choices
    def get_choices(self):
        return self._choices.all()
        
    # Clear choices
    def clear_choices(self):
        self._remove_children('_choices')
        
    # Randomize choice order
    def randomize(self, randomize=True):
        self._randomize_children('_choices')
    
    
    # VALIDATORS
    # Get list of validators
    def get_validators(self):
        return self._validators.all()
        
    # Clear validators
    def clear_validators(self):
        self._remove_children('_validators')
    
    
        
    ##########################################################################
    # Columns
    ##########################################################################
    
    # TEXT
    # Set question text
    # to remove, text()
    def text(self, text=''):
        self._set_text(text)

    # Gets the question text
    def get_text(self):
        return self._text
    
    
    # ALL ROWS
    # Set the all_rows indicator
    # i.e. the data will appear in all of the participant's dataframe rows
    # True = on, False = off
    def all_rows(self, all_rows=True):
        self._all_rows = all_rows
        
    # Get all_rows indicator
    def get_all_rows(self):
        return self._all_rows
        
    
    # QUESTION TYPE
    # Set question type
    def qtype(self, qtype='text'):
        self._qtype = qtype
        
    # Get question type
    def get_qtype(self):
        return self._qtype
    
    
    # VARIABLE
    # Set the variable in which question data will be stored
    def var(self, var=None):
        self._var = var
        
    # Get variable
    def get_var(self):
        return self._var
        
    
    # DEFAULT
    # Set default answer
    # string for free response type
    # choice id for choice types
    def default(self, default=None):
        self._default_is_choice = type(default) == Choice
        if self._default_is_choice:
            default = default.id
        self._init_default = self._default = default
        
    # Get default
    def get_default(self):
        if self._default_is_choice:
            return Choice.query.get(self._default)
        return self._default
        
    # Reset default to initial default
    # typically for use after invalid page submission
    def reset_default(self):
        self.default(self._init_default)
        
    
    # COMPILE FUNCTION AND ARGUMENTS  
    # Set the compile function and arguments
    # to clear function and args, compile()
    def compile(self, compile=None, args=None):
        self._set_function('_compile_function', compile, '_compile_args', args)
        
    # Return the compile function
    def get_compile(self):
        return self._compile_function
        
    # Return the compile function arguments
    def get_compile_args(self):
        return self._compile_args
        
        
    # POST FUNCTION AND ARGUMENTS
    # Set the post function and arguments
    def post(self, post=None, args=None):
        self._set_function('_post_function', post, '_post_args', args)
        
    # Return the post function
    def get_post(self):
        return self._post_function
        
    # Return the post function arguments
    def get_post_args(self):
        return self._post_args
    
    
    # DEBUG FUNCTION AND ARGUMENTS
    # Set the debug function and arguments
    def debug(self, debug=None, args=None, attrs=None):
        self._set_function(
            '_debug_function', debug, 
            '_debug_args', args, 
            '_debug_attrs', attrs)
    
    # Get the debug function
    def get_debug(self):
        return self._debug_function
    
    # Get the debug function arguments
    def get_debug_args(self):
        return self._debug_args
    
    # Get the Debug Page attributes
    def get_debug_attrs(self):
        return self._debug_attrs
    
    
    # DATA, RESPONSE, AND ERROR
    # Set the question data
    def data(self, data=None):
        self._data = data
        
    # Get the question data
    def get_data(self):
        return self._data
        
    # Get the question response
    def get_response(self):
        return self._response
        
    # Get the list of selected choices
    def get_selected(self):
        return [c for c in self._choices if c._checked=='checked']
        
    # Get the list of nonselected choices
    def get_nonselected(self):
        return [c for c in self._choices if c._checked=='']
        
    # Set the question error message
    def error(self, message=None):
        self._error = message
        
    # Get the question error message
    def get_error(self):
        return self._error
    
        
    
    ##########################################################################
    # Private methods
    ##########################################################################
        
    # Record the participant's response
    # collect response and update default
    def _record_response(self, response):
        if self._qtype == 'free':
            self._default = response
        else:
            [c._set_checked(response=='c'+str(c.id)) for c in self._choices]
            checked = self.get_selected()
            if checked:
                response = checked[0].get_value()
                self._default = checked[0].id
        self._response = response
        self.data(response)
        
    # Validate the participant's response
    def _validate(self):
        for v in self._validators:
            self._error = v._get_error()
            if self._error is not None:
                return False
        return True
        
    # Set the variable order
    def _set_vorder(self, i):
        self._vorder = i
        
    # Output the data (both question data and order data)
    # data consists of:
    # main data (usually referred to simply as 'data')
    # page (or branch) order: order in which question appeared its page
    # variable order: order in which question appeared
    #   relative to other questions belonging to the same variable
    # choice order for each choice
    def _output_data(self):
        if self._part is None or self._var is None:
            return {}
    
        data = {
            self._var: self._data,
            self._var+'_porder': self._index,
            self._var+'_vorder': self._vorder}
            
        for c in self._choices:
            data['_'.join([self._var,c.get_label(),'qorder'])] = c._index
            
        return data