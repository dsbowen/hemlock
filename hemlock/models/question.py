###############################################################################
# Question model
# by Dillon Bowen
# last modified 02/10/2019
###############################################################################

from hemlock import db
from hemlock.models.choice import Choice
from hemlock.models.validator import Validator
from hemlock.models.base import Base
from random import shuffle

# Renders errors from previous submit
def render_error(q):
    if q.error is None:
        return ''
    return '''
        <div style='color: #ff0000;'>
        {0}
        </div>
        '''.format(q.error)

# Renders question text in html format
def render_text(q):
    return '''
        {0}
        <br></br>
        '''.format(q.text)
        
# Renders the question body in html format
def render_body(q):
    if q.qtype == 'text':
        return ''
    if q.qtype == 'free':
        return render_free(q)
    if q.qtype == 'single choice':
        return render_single_choice(q)
    
# Renders free response question in html format
def render_free(q):
    return '''
        <input name='{0}' type='text' value='{1}'>
        '''.format(q.id, q.default)
    
# Renders single choice question in html format
def render_single_choice(q):
    choices = q.choices.order_by('order').all()
    if q.randomize:
        shuffle(choices)
    choice_html = ['''
        <input name='{0}' type='radio' value='{1}'>{2}
        <br></br>
        '''.format(q.id, c.value, c.text) for c in choices]
    return ''.join(choice_html)

# Data:
# ID of participant to whom the question belongs
# ID of the branch to which the question belongs (for embedded data only)
# ID of the page to which the question belongs
# Question type (qtype)
# Variable in which the question data will be stored
# Text
# Default answer
# Data
# Order in which question appears on page
# All_rows indicator
#   i.e. the question data will appear in all of its participant's rows
class Question(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    choices = db.relationship('Choice', backref='question', lazy='dynamic')
    validators = db.relationship('Validator', backref='question', lazy='dynamic')
    qtype = db.Column(db.String(16))
    var = db.Column(db.Text)
    text = db.Column(db.Text)
    randomize = db.Column(db.Boolean)
    default = db.Column(db.Text)
    entry = db.Column(db.Text)
    data = db.Column(db.PickleType)
    rendered = db.Column(db.Boolean)
    render_function = db.Column(db.PickleType)
    render_args = db.Column(db.PickleType)
    post_function = db.Column(db.PickleType)
    post_args = db.Column(db.PickleType)
    order = db.Column(db.Integer)
    error = db.Column(db.PickleType)
    all_rows = db.Column(db.Boolean)
    
    # Adds question to database and commits on initialization
    def __init__(self, branch=None, page=None, order=None, var=None, 
        qtype='text', text='', randomize=False, default='', data=None, render=None, render_args=None, post=None, post_args=None, all_rows=False):
        
        self.set_qtype(qtype)
        self.branch = branch
        self.assign_page(page, order)
        self.set_var(var)
        self.set_text(text)
        self.set_randomize(randomize)
        self.set_default(default)
        self.set_data(data)
        self.set_render(render, render_args)
        self.set_post(post, post_args)
        self.set_all_rows(all_rows)
        db.session.add(self)
        db.session.commit()
    
    # Assign to page
    # question is assigned to end of queue by default
    def assign_page(self, page, order=None):
        if page is not None:
            self.assign_parent('page', page, page.questions.all(), order)
        
    # Remove from page
    def remove_page(self):
        if self.page is not None:
            self.remove_parent('page', self.page.questions.all())
        
    # Set question type (default text only)
    def set_qtype(self, qtype):
        self.qtype = qtype
    
    # Set default answer
    def set_default(self, default):
        self.default = default
        
    # Records the participant's entry
    def record_entry(self, entry):
        self.entry = entry
        self.set_data(entry)
        if self.qtype == 'single choice':
            [c.set_selected() for c in self.choices if entry==str(c.value)]
        
    # Set the data
    def set_data(self, data):
        self.data = data
        
    def get_selected(self):
        return [c for c in self.choices if c.selected]
        
    def get_nonselected(self):
        return [c for c in self.choices if not c.selected]
        
    # Render the question in html
    # assign to participant upon rendering
    def render_html(self):
        if not self.rendered:
            self.rendered = True
            self.call_function(self, self.render_function, self.render_args)
        
        if self.qtype == 'embedded':
            return ''
            
        return '''
        <p>
            {0}
            {1}
            {2}
        </p>
        '''.format(render_error(self), render_text(self), render_body(self))
        
    # Validate an answer
    def validate(self, part):
        self.assign_participant(part)
        errors = [v.get_error() for v in self.validators]
        self.error = next(iter([e for e in errors if e is not None]), None)
        return self.error is None