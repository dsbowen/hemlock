"""Embedded question polymorph"""

from hemlock.question_polymorphs.imports import *


class Embedded(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'embedded'}
    
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    
    def __init__(self, page=None, **kwargs):
        super().__init__(['embedded_settings'], page, **kwargs)
        
    def set_branch(self, branch, index=None):
        self._set_parent(branch, index, 'branch', 'embedded')
    
    def _render(self):
        return ''
    
    def _record_response(self, response):
        return
        
    def _record_data(self):
        return