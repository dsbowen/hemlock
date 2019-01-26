###############################################################################
# Question model
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import db
from hemlock.models.choice import Choice

# Renders question text in html format
def render_text(q):
    return '<div>\n' + q.text + '\n<br></br>\n</div>\n'
    
# Renders free response question in html format
def render_free(q):
    html = '\n<div>\n    '
    html += "<input name='" + str(q.id) + "' type='text' value='" + q.default + "'>"
    html += "\n</div>\n"
    return html
    
# Renders single choice question in html format
def render_single_choice(q):
    html = ''
    for choice in q.choices:
        html += '\n<div>\n'
        html += "<input name='" + str(q.id) + "'"
        html += "type='radio'"
        html += "value='" + str(choice.value) + "'>"
        html += choice.text
        html += '\n</div>\n'
    return html

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
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    choices = db.relationship('Choice', backref='question', lazy='dynamic')
    qtype = db.Column(db.String(16))
    var = db.Column(db.Text)
    text = db.Column(db.Text)
    default = db.Column(db.Text)
    data = db.Column(db.Text)
    order = db.Column(db.Integer)
    all_rows = db.Column(db.Boolean)
    
    # Adds question to database and commits on initialization
    def __init__(self, branch=None, page=None, order=None, var=None, qtype='text', text='', default='',
        data=None, all_rows=False):
        
        self.set_qtype(qtype)
        self.branch = branch
        self.assign_page(page, order)
        self.set_var(var)
        self.set_text(text)
        self.set_default(default)
        self.set_data(data)
        self.set_all_rows(all_rows)
        db.session.add(self)
        db.session.commit()
    
    # Assign to page
    # removes question from old page (if any)
    # assigns question to new page
    # adds itself to the new page question list (default at end)
    def assign_page(self, page, order=None):
        if self.page:
            self.page.remove_question(self)
        self.page = page
        self.set_order(order)
        
    # Set the order in which the question appears in its page
    # appears at the end of the page by default
    def set_order(self, order=None):
        if order is None and self.page:
            order = len(self.page.questions.all()) - 1
        self.order = order
        
    # Set the variable in which question data will be stored
    def set_var(self, var):
        self.var = var
        
    # Set question type (default text only)
    def set_qtype(self, qtype):
        self.qtype = qtype
    
    # Set text
    def set_text(self, text):
        self.text = text
        
    # Add choice
    def add_choice(self, text='', value=None):
        choice = Choice(question=self, text=text, value=value)
    
    # Set default answer
    def set_default(self, default):
        self.default = default
        
    # Set the data
    def set_data(self, data):
        self.data = data
        
    # Set the all_rows indicator
    # i.e. the question data will appear in all of its participant's rows
    def set_all_rows(self, all_rows):
        self.all_rows = all_rows
        
    # Render the question in html
    # assign to participant upon rendering
    def render(self, part):
        self.part = part
        db.session.commit()
        
        if self.qtype == 'embedded':
            return ''
        
        rendered_html = '\n<p>\n' + render_text(self)
        if self.qtype == 'free':
            rendered_html += render_free(self)
        if self.qtype == 'single choice':
            rendered_html += render_single_choice(self)
        return rendered_html + '</p>\n'