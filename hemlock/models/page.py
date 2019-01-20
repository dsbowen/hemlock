from flask import request
from hemlock import db
from hemlock.models.question import Question
from random import choice
from string import ascii_letters, digits

def hidden_tag():
    tag = ''.join([choice(ascii_letters + digits) for i in range(90)])
    return "<input name='crsf_token' type='hidden' value='" + tag + "'>"

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    questions = db.relationship('Question', backref='page', lazy='dynamic')
    valid = db.Column(db.Boolean, default=False)
    terminal = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer)
    
    def __init__(self, branch=None, order=None, terminal=False):
        self.assign_branch(branch, order)
        self.set_terminal(terminal)
        db.session.add(self)
        db.session.commit()
    
    def assign_branch(self, branch, order=None):
        if self.branch:
            self.branch.remove_page(self)
        self.branch = branch
        self.set_order(order)
        
    def set_order(self, order=None):
        if order is None and self.branch:
            order = len(self.branch.page_queue.all()) - 1
        self.order = order
        
    def set_terminal(self, terminal=True):
        self.terminal = terminal
        
    def remove_question(self, question):
        self.questions.remove(question)
        questions = self.questions.order_by('order')
        for i in range(len(self.questions.all())):
            questions[i].set_order(i)
    
    def render(self):
        rendered_html = hidden_tag()
        for question in self.questions.order_by('order'):
            rendered_html += question.render(self.part)
        if not self.terminal:
            rendered_html += "<p align=right><input type='submit' name='submit' value='>>'></p>"
        return rendered_html
        
    def validate_on_submit(self):
        if request.method == 'POST':    
            for question in self.questions:
                question.set_data(request.form.get(str(question.id)))
                # ADD QUESTION VALIDATION HERE
        return request.method == 'POST'