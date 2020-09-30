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
from sqlalchemy_mutablesoup import MutableSoup

import json
import time


class ChoiceBase():
    def __init__(self, label, template, **kwargs):
        from ..tools import key

        self.id = key(10)
        self.body = MutableSoup(
            render_template(template, self_=self), 'html.parser'
        )
        self.label = label
        self.name = kwargs['name'] if 'name' in kwargs else label
        self.value = kwargs['value'] if 'value' in kwargs else label

    def is_default(self, question):
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
        default = (
            question.response if question._has_responded 
            else question.default
        )
        if not default:
            return False
        return (
            self.value in default if isinstance(default, list)
            else self.value == default
        )

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


class Choice(ChoiceBase):
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
    def __init__(self, label='', template='hemlock/choice.html', **kwargs):
        super().__init__(label, template, **kwargs)

    @property
    def label(self):
        return self.body.text('label.choice')

    @label.setter
    def label(self, val):
        self.body.set_element('label.choice', val)

    def select(self, driver):
        self._click(driver, if_selected=False)

    def deselect(self, driver):
        self._click(driver, if_selected=True)

    def _click(self, driver, if_selected):
        inpt = driver.find_element_by_css_selector('#'+self.id)
        if if_selected == bool(inpt.get_attribute('checked')):
            selector = 'label[for={}]'.format(self.id)
            label = driver.find_element_by_css_selector(selector)
            try:
                label.click()
            except:
                time.sleep(.5)
                label.click()
    
    def _render(self, question, idx, body=None):
        """Render the choice HTML

        Set the input name to reference the quesiton `model_id`. Then set 
        the `checked` attribute to reflect whether the choice is a default.
        """
        def handle_multiple():
            """
            Adds appropriate classes depending on whether users can select 
            multiple choices
            """
            div = body.select_one('div.custom-control')
            div_class = div['class']
            rm_classes = (
                'custom-radio', 'custom-checkbox', 'custom-control-inline'
            )
            div_class = [c for c in div_class if c not in rm_classes]
            if question.multiple:
                div_class.append('custom-checkbox')
                inpt['type'] = 'checkbox'
            else:
                div_class.append('custom-radio')
                inpt['type'] = 'radio'
            if question.inline:
                div_class.append('custom-control-inline')
            div['class'] = div_class

        def handle_default():
            if self.is_default(question):
                inpt['checked'] = None
            else:
                inpt.attrs.pop('checked', None)

        body = body or self.body.copy()
        inpt = body.select_one('input')
        inpt['name'] = question.model_id
        inpt['value'] = idx
        handle_multiple()
        handle_default()
        return body
            

class Option(ChoiceBase):
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

    def __init__(self, label='', template='hemlock/option.html', **kwargs):
        super().__init__(label, template, **kwargs)

    @property
    def label(self):
        return self.body.text('option')
    
    @label.setter
    def label(self, val):
        self.body.set_element('option', val)

    def select(self, driver):
        self._click(driver, if_selected=False)

    def deselect(self, driver):
        self._click(driver, if_selected=True)

    def _click(self, driver, if_selected):
        option = driver.find_element_by_css_selector('#'+self.id)
        if if_selected == bool(option.get_attribute('selected')):
            try:
                option.click()
            except:
                time.sleep(.5)
                option.click()
    
    def _render(self, question, idx, body=None):
        def handle_default():
            if self.is_default(question):
                option['selected'] = None
            else:
                option.attrs.pop('selected', None)

        body = body or self.body.copy()
        option = body.select_one('option')
        option['name'] = question.model_id
        option['value'] = idx
        handle_default()
        return body