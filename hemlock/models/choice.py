"""# Choices and Options

The difference between `hemlock.Choice` and `hemlock.Option` is the former are 
for `hemlock.Check` questions, while latter are for `hemlock.Select` questions.

The use of choice and option models is not due to any deep functional 
difference between them, but reflects the underlying html.
"""

from ..app import db
from .bases import HTMLMixin, InputBase

from flask import render_template
from sqlalchemy_mutable import MutableType


class Choice(InputBase, HTMLMixin, db.Model):
    """
    Choices are displayed as part of their question in index order.

    It inherits from 
    [`hemlock.models.InputBase` and `hemlock.models.HTMLMixin`](bases.md).

    Parameters
    ----------
    label : str, default=''
        Choice label.

    template : str, default='choice.html'
        Template for the choice `body`.

    Attributes
    ----------
    index : int or None, default=None
        Order in which this choice appears in its question.

    label : str, default=''
        The choice label.

    name : str or None, default=None
        Name of the choice column in the dataframe.

    value : sqlalchemy_mutable.MutableType or None, default=None
        Value of the data associated with the choice. For a question where 
        only one choice can be selected, this is the value of the question's 
        data if this choice is selected. For a question where multiple 
        choices may be selected, data are one-hot encoded; the value is the 
        suffix of the column name associated with the indicator variable that 
        this choice was selected.

    Relationships
    -------------
    question : hemlock.Question
        The question to which this choice belongs.

    Notes
    -----
    Passing `label` into the constructor is equivalent to calling 
    `self.set_all(label)` unless `name` and `value` arguments are also passed
    to the constructor.
    """
    id = db.Column(db.Integer, primary_key=True)
    choice_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'choice',
        'polymorphic_on': choice_type
    }
    
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    index = db.Column(db.Integer)
    value = db.Column(MutableType)
    
    def __init__(self, label='', template='hemlock/choice.html', **kwargs):
        super().__init__(template, label=label, **kwargs)
        if 'name' not in kwargs:
            self.name = self.label
        if 'value' not in kwargs:
            self.value = self.label

    @property
    def label(self):
        return self.body.text('label.choice')

    @label.setter
    def label(self, val):
        self.body.set_element('label.choice', val)

    def set_all(self, val):
        """
        Set the choice's label, name, and value.

        Parameters
        ----------
        val : 
            Value to which the choice's label, name, and value should be set.

        Returns
        -------
        self : hemlock.Choice
        """
        self.label = self.name = self.value = val
        return self
    
    def is_default(self):
        """
        Returns
        -------
        is_default : bool
            Indicate that this choice is (one of) its question's default 
            choice(s).

        Notes
        -----
        The question's default choice(s) is the question's `response`, if not 
        `None`, or the question's `default`.
        """
        if self.question is None:
            return False
        default = self.question.response or self.question.default
        if isinstance(default, list):
            return self in default
        return self == default
    
    def _render(self, body=None):
        """Render the choice HTML

        Set the input name to reference the quesiton `model_id`. Then set 
        the `checked` attribute to reflect whether the choice is a default.
        """
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
        """Appropriately converts body HTML for single or multiple choice"""
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
    """
    Options are a choice polymorph for `hemlock.Select` questions.

    Inherits from `hemlock.Choice`.

    Parameters
    ----------
    label : str, default=''
        Option label.

    template : str, default='hemlock/option.html'
        Template for the option `body`.
    """
    id = db.Column(db.Integer, db.ForeignKey('choice.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'option'}

    def __init__(self, label='', template='hemlock/option.html', **kwargs):
        super().__init__(label, template, **kwargs)

    @property
    def label(self):
        return self.body.text('option')
    
    @label.setter
    def label(self, val):
        self.body.set_element('option', val)
    
    def _render(self, body=None):
        body = body or self.body.copy()
        opt_tag = body.select_one('#'+self.model_id)
        opt_tag['name'] = self.question.model_id
        if self.is_default():
            opt_tag['selected'] = None
        else:
            opt_tag.attrs.pop('selected', None)
        return body