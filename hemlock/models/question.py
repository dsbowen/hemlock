"""# Questions

`hemlock.Question` and `hemlock.ChoiceQuestion` are 'question skeletons';
most useful when fleshed out. See section on question polymorphs.
"""

from ..app import db
from ..tools import key
from .bases import Data

from flask import render_template, request
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy_mutable import (
    HTMLAttrsType, MutableType, MutableJSONType, MutableListType, 
    MutableListJSONType
)

import html
import os
from copy import copy


class Question(Data):
    """
    Base object for questions. Questions are displayed on their page in index 
    order.

    It inherits from 
    [`hemlock.models.Data` and `hemlock.models.HTMLMixin`](bases.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Question label.

    template : str, default='form-group.html'
        Template for the question `body`.

    Attributes
    ----------
    default : sqlalchemy_mutable.MutableType
        Default question response.

    error : str or None, default=None
        Text of the question error message.

    label : str or None, default=None
        Question label.

    response : sqlalchemy_mutable.MutableType
        Participant's response.

    Relationships
    -------------
    part : hemlock.Participant or None
        The participant to which this question belongs. Derived from 
        `self.page`.

    branch : hemlock.Branch or None
        The branch to which this question belongs. Derived from `self.page`.

    page : hemlock.Page or None
        The page to which this question belongs.

    compile : list of hemlock.Compile, default=[]
        List of compile functions; run before the question is rendered.

    validate : list of hemlock.Validate, default=[]
        List of validate functions; run to validate the participant's response.

    submit : list of hemlock.Submit, default=[]
        List of submit functions; run after the participant's responses have been validated for all questions on a page.

    debug : list of hemlock.Debug, default=[]
        List of debug functions; run during debugging. The default debug function is unique to the question type.
    """
    id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
    question_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'polymorphic_on': question_type
    }

    # relationships
    @property
    def part(self):
        return None if self.page is None else self.page.part

    @property
    def branch(self):
        return None if self.page is None else self.page.branch

    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    # HTML attributes
    key = db.Column(db.String(10))
    template = db.Column(db.String)
    css = db.Column(MutableListJSONType, default=[])
    js = db.Column(MutableListJSONType, default=[])
    form_group_class = db.Column(MutableListJSONType, default=[])
    form_group_attrs = db.Column(HTMLAttrsType, default={})
    error = db.Column(db.Text)
    error_attrs = db.Column(HTMLAttrsType, default={})
    label = db.Column(db.Text)
    prepend = db.Column(db.String)
    append = db.Column(db.String)
    input_attrs = db.Column(HTMLAttrsType)

    # Function attributes
    compile = db.Column(MutableListType, default=[])
    debug = db.Column(MutableListType, default=[])
    validate = db.Column(MutableListType, default=[])
    submit = db.Column(MutableListType, default=[])

    # Additional attributes
    default = db.Column(MutableJSONType)
    response = db.Column(MutableJSONType)
    has_responded = db.Column(db.Boolean, default=False)

    def __init__(
            self, label=None, extra_css=[], extra_js=[], 
            form_group_class=['card', 'form-group', 'question'],
            form_group_attrs={}, 
            error_attrs={'style': {'color': 'rgb(114,28,36)'}}, 
            **kwargs
        ):
        def add_extra(attr, extra):
            # add extra css or javascript
            if extra:
                assert isinstance(extra, (str, list))
                if isinstance(extra, str):
                    attr.append(extra)
                else:
                    attr += extra

        self.key = key(10)
        self.compile, self.debug, self.validate, self.submit = [], [], [], []
        self.css, self.js = [], []
        super().__init__(
            label=label, 
            form_group_class=form_group_class,
            form_group_attrs=form_group_attrs,
            error_attrs=error_attrs, 
            **kwargs
        )
        add_extra(self.css, extra_css)
        add_extra(self.js, extra_js)

    # methods
    def clear_error(self):
        """
        Clear the error message.

        Returns
        -------
        self : hemlock.Question
        """
        self.error = None
        return self

    def clear_response(self):
        """
        Clear the response.

        Returns
        -------
        self : hemlock.Question
        """
        self.response = None
        self.has_responded = False
        return self

    # methods executed during study
    def _compile(self):
        [f(self) for f in self.compile]
        return self

    def _render(self, body=None):
        return render_template(self.template, q=self)

    def _render_js(self):
        return '\n'.join(self.js)

    def _record_response(self):
        self.has_responded = True
        self.response = request.form.get(self.key)
        if isinstance(self.response, str):
            # convert to safe html
            self.response = html.escape(self.response)
        return self
        
    def _validate(self):
        """Validate Participant response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        for f in self.validate:
            self.error = f(self)
            if self.error:
                return False
        self.error = None
        return True

    def _record_data(self):
        self.data = self.response
        return self
    
    def _submit(self):
        [f(self) for f in self.submit]
        return self

    def _debug(self, driver):
        [f(driver, self) for f in self.debug]
        return self


class ChoiceQuestion(Question):
    """
    A question which contains choices. Inherits from `hemlock.Question`.

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Question label.

    choices : list, default=[]
        Choices which belong to this question. List items are usually 
        `hemlock.Choice` or `hemlock.Option`.

    template : str or None, default=None
        Template for the question body.

    Attributes
    ----------
    choices : list, default=[]
        Set from `choices` parameter.

    choice_cls : class, default=hemlock.Choice
        Class of the choices in the `choices` list.

    multiple : bool, default=False
        Indicates that the participant can select multiple choices.

    Notes
    -----
    `choices` can be set using the following formats:
    1. list of choice objects.
    2. list of `str`, treated as choice labels.
    3. list of `(choice label, value)` tuples.
    4. list of `(choice label, value, name)` tuples.
    5. list of dictionaries with choice keyword arguments.
    """
    choices = None # must be implemented by choice question

    def __init__(self, label=None, choices=[], template=None, **kwargs):
        self.choices = choices
        super().__init__(label=label, template=template, **kwargs)

    def _render(self, body=None):
        """Add choice HTML to `body`"""
        return render_template(self.template, q=self)

    def _record_response(self):
        """Record response

        The response is a single choice or a list of choices (if multiple 
        choices are allowed).
        """
        self.has_responded = True
        idx = request.form.getlist(self.key)
        self.response = [self.choices[int(i)].value for i in idx]
        if not self.multiple:
            self.response = self.response[0] if self.response else None
        return self

    def _record_data(self):
        """Record data

        For single choice questions, the data is the selected choice's 
        `value`.

        For multiple choice questions, the data is a dictionary mapping 
        each choice's `value` to a binary indicator that it was selected.
        """
        if self.multiple:
            self.data = {
                choice.value: int(choice.value in self.response)
                for choice in self.choices
            }
        else:
            self.data = self.response
        return self
    
    def _pack_data(self):
        """Pack data for storage in the `DataStore`

        For multiple choice questions, the packed data dictionary is similar to the data, but with the question's variable prepended to the key.
        """
        var = self.var
        if not self.multiple or var is None:
            return super()._pack_data()
        if self.data is None:
            packed_data = {
                var+c.value: None 
                for c in self.choices if c.value is not None
            }
        elif isinstance(self.data, dict):
            packed_data = {var+key: val for key, val in self.data.items()}
        else:
            packed_data = self.data
        return super()._pack_data(packed_data)