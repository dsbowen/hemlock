"""Embedded question polymorph"""

from hemlock.question_polymorphs.imports import *


class Embedded(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'embedded'}
    
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    
    def __init__(self, branch=None, index=None, *args, **kwargs):
        self.set_branch(branch, index)
        super().__init__(*args, **kwargs)
        
    def set_branch(self, branch, index=None):
        self._set_parent(branch, index, 'branch', 'embedded')
    
    def _compile(self):
        return ''
    
    def _record_response(self, response):
        return
        
    def _submit(self):
        return