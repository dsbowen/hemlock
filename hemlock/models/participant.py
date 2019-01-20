from hemlock import db
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.variable import Variable

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_stack = db.relationship('Branch', backref='part', lazy='dynamic')
    curr_page = db.relationship('Page', uselist=False, backref='part')
    questions = db.relationship('Question', backref='part', lazy='dynamic')
    variables = db.relationship('Variable', backref='part', lazy='dynamic')
    
    def __init__(self):
        db.session.add(self)
        db.session.commit()
        
    def get_page(self):
        return self.curr_page
        
    def advance_page(self):
        if not self.branch_stack.all():
            return False
        branch = self.branch_stack[-1]
        page = branch.dequeue()
        if page is None:
            self.terminate_branch(branch)
            return self.advance_page()
        self.curr_page = page
        return True
        
    def terminate_branch(self, branch):
        new_branch = branch.get_next()
        self.branch_stack.remove(branch)
        db.session.delete(branch)
        db.session.commit()
        if new_branch is not None:
            new_branch.part = self
            
    def store_data(self):
        for question in self.questions:
            if question.var:
                self.process_question(question)
        self.clear_memory()
        
    def process_question(self, question):
        var = Variable.query.filter_by(part_id=self.id, name=question.var).first()
        if not var:
            var = Variable(part=self, name=question.var)
        var.add_data(question.data)
        return str(var.data)
        
    def clear_memory(self):
        for branch in Branch.query.filter_by(part_id=self.id).all():
            db.session.delete(branch)
        for page in Page.query.filter_by(part_id=self.id).all():
            if page != self.curr_page:
                db.session.delete(page)
        for question in Question.query.filter_by(part_id=self.id).all():
            if question not in self.curr_page.questions:
                db.session.delete(question)
        db.session.commit()