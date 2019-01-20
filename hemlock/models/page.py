from hemlock import db
from hemlock.models.question import Question
from random import choice
from string import ascii_letters, digits

def hidden_tag():
    tag = ''.join([choice(ascii_letters + digits) for i in range(90)])
    return "<input name='crsf_token' type='hidden' value='" + tag + "'>"

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant = db.relationship('Participant', backref='curr_page', lazy='dynamic')
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    questions = db.relationship('Question', backref='page', lazy='dynamic')
    valid = db.Column(db.Boolean, default=False)
    terminal = db.Column(db.Boolean, default=False)
    
    def assign_branch(self, branch):
        self.branch = branch
        
    def set_terminal(self, terminal=True):
        self.terminal = terminal
    
    def render(self):
        rendered_html = hidden_tag()
        for question in self.questions:
            rendered_html += question.render()
        if not self.terminal:
            rendered_html += "<p align=right><input type='submit' name='submit' value='>>'></p>"
        return rendered_html
        
    def validate_on_submit(self):
        return True