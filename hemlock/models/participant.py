from hemlock import db
from hemlock.models.branch import Branch
from hemlock.models.page import Page
import survey

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_stack = db.relationship('Branch', backref='part', lazy='dynamic')
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
        
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
        next = branch.get_next()
        self.branch_stack.remove(branch)
        if next is not None:
            new_branch = getattr(survey, next)()
            new_branch.part = self