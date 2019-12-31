"""Choice database model"""

from hemlock.app import db
from hemlock.database.bases import HTMLMixin, InputBase

from flask import render_template
from sqlalchemy_mutable import MutableType


class Choice(InputBase, HTMLMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'choice',
        'polymorphic_on': type
    }
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    index = db.Column(db.Integer)    
    name = db.Column(db.Text)
    value = db.Column(MutableType)
    
    @HTMLMixin.init('Choice')
    def __init__(self, question=None, **kwargs):
        super().__init__()
        self.body = render_template('choice.html', c=self)
        self.set_all(kwargs.pop('label', None))
        return {'question': question, **kwargs}

    @property
    def label(self):
        return self.body.text('label.choice')

    @label.setter
    def label(self, val):
        self.body._set_element('label.choice', val)

    def set_all(self, val):
        self.label = self.name = self.value = val
    
    def is_default(self):
        """Indicate if self is a default choice

        Default is assumed to a be a choice or list of choices.
        """
        if self.question is None:
            return False
        default = self.question.response or self.question.default
        if isinstance(default, list):
            return self in default
        return self == default
    
    def _render(self, body=None):
        body = body or self.body.copy()
        inpt = body.select_one('input#'+self.model_id)
        inpt['name'] = self.question.model_id
        self._handle_multiple(body, inpt)
        if self.is_default():
            inpt['checked'] = None
        else:
            inpt.attrs.pop('checked', None)
        return body

    def _handle_multiple(self, body, inpt):
        """Appropriately converts body html for single or multiple choice"""
        div_class = body.select_one('div.custom-control')['class']
        rm_classes = [
            'custom-radio', 'custom-checkbox', 'custom-control-inline'
        ]
        for class_ in rm_classes:
            try:
                div_class.remove(class_)
            except:
                pass
        if not self.question.multiple:
            div_class.append('custom-radio')
            inpt['type'] = 'radio'
        else:
            div_class.append('custom-checkbox')
            inpt['type'] = 'checkbox'
        if self.question.inline:
            div_class.append('custom-control-inline')
            

class Option(Choice):
    id = db.Column(db.Integer, db.ForeignKey('choice.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'option'}

    @Choice.init('Option')
    def __init__(self, question=None, **kwargs):
        super(HTMLMixin, self).__init__()
        self.body = render_template('option.html', opt=self)
        self.set_all(kwargs.pop('label', None))
        return {'question': question, **kwargs}

    @property
    def label(self):
        return self.body.text('option')
    
    @label.setter
    def label(self, val):
        self.body._set_element('option', val)
    
    def _render(self, body=None):
        body = body or self.body.copy()
        opt_tag = body.select_one('#'+self.model_id)
        opt_tag['name'] = self.question.model_id
        if self.is_default():
            opt_tag['selected'] = None
        else:
            opt_tag.attrs.pop('selected', None)
        return body