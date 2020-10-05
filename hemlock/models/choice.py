"""# Choices and Options

The difference between `hemlock.Choice` and `hemlock.Option` is the former are 
for `hemlock.Check` questions, while latter are for `hemlock.Select` questions.

The use of choice and option models is not due to any deep functional 
difference between them, but reflects the underlying html.
"""

from ..app import db
from .bases import HTMLMixin

from flask import render_template
from sqlalchemy_mutable import MutableType
from sqlalchemy_mutablesoup import MutableSoup

import json
import time


class ChoiceBase():
    """
    Base class for choices.

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Choice label.

    template : str
        Jinja template for the choice html. The choice object is passed to the
        template as a parameter named `self_`.

    value : default=None
        Value of the choice if selected. e.g. a choice with label `'Yes'` 
        might have a value of `1`. If `None`, the `label` is used. For a 
        question where only one choice can be selected, this is the value of 
        the question's data if this choice is selected. For a question where 
        multiple choices may be selected, data are one-hot encoded; the value 
        is the suffix of the column name associated with the indicator 
        variable that this choice was selected.

    name : default=None
        Name associated with this choice in the dataframe. If `None`, the 
        `label` is used.

    Attributes
    ----------
    id : str
        Randomly generated from ascii letters and digits.

    body : bs4.BeautifulSoup
        Choice html created from the `template` parameter.

    label : str or bs4.BeautifulSoup
        Set from the `label` parameter.

    value : 
        Set from the `value` parameter.

    name :
        Set from the `name` parameter.

    Notes
    -----
    If passing `value` and `name` to contructor, these must be passed as 
    keyword arguments
    """
    def __init__(self, label, template, **kwargs):
        from ..tools import key

        self.id = key(10)
        self.body = MutableSoup(
            render_template(template, self_=self), 'html.parser'
        )
        self.label = label
        self.value = kwargs['value'] if 'value' in kwargs else label
        self.name = kwargs['name'] if 'name' in kwargs else label

    def is_default(self, question):
        """
        Parameters
        ----------
        question : hemlock.Question
            The question to which this choice belongs.

        Returns
        -------
        is_default : bool
            Indicate that this choice is (one of) its question's default 
            choice(s).

        Notes
        -----
        The question's default choice(s) is the question's `response` if the 
        participant responded to the question, or the question's `default` if
        the participant has not yet responded to the question.
        """
        default = (
            question.response if question.has_responded else question.default
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
    Choices are displayed as part of their question (usually 
    `hemlock.Check`). Inherits from `hemlock.ChoiceBase`.

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Choice label.

    template : str, default='hemlock/choice.html'
        Template for the choice `body`.

    \*\*kwargs :
        Set the choice's value and name using keyword arguments.
    """    
    def __init__(self, label='', template='hemlock/choice.html', **kwargs):
        super().__init__(label, template, **kwargs)

    @property
    def label(self):
        return self.body.text('label.choice')

    @label.setter
    def label(self, val):
        self.body.set_element('label.choice', val)

    def click(self, driver, if_selected=None):
        """
        Use a selenium webdriver to click on this choice.

        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver
            The selenium webdriver that clicks this choice. Does not have to 
            be chromedriver.

        if_selected : bool or None, default=None
            Indicates that the choice will be clicked only if it is already 
            selected. If `False` the choice will be clicked only if it is not 
            already selected. If `None` the choice will be clicked whether or 
            not it is selected.

        Returns
        -------
        self
        """
        inpt = driver.find_element_by_css_selector('#'+self.id)
        if (
            if_selected is None
            or if_selected == bool(inpt.get_attribute('checked'))
        ):
            selector = 'label[for={}]'.format(self.id)
            driver.find_element_by_css_selector(selector).click()
        return self

    def is_displayed(self, driver):
        """
        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver
            The selenium webdriver that clicks this choice. Does not have to 
            be chromedriver.

        Returns
        -------
        is_displayed : bool
            Indicates that this choice is visible in the browser.
        """
        selector = 'label[for={}]'.format(self.id)
        label = driver.find_element_by_css_selector(selector)
        return label.is_displayed()
    
    def _render(self, question, idx, body=None):
        """Render the choice HTML
        
        Parameters
        ----------
        question : hemlock.Question
            Question to which this choice belongs.

        idx : int
            Index of this choice in the question's `choices` list.
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
    Options are displayed as part of their question (usually 
    `hemlock.Select`). Inherits from `hemlock.ChoiceBase`. Its functionality
    is similar to `hemlock.Choice`, but for `Select` questions instead of
    `Check` questions.

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Choice label.

    template : str, default='hemlock/option.html'
        Template for the choice `body`.

    \*\*kwargs :
        Set the choice's value and name using keyword arguments.
    """
    def __init__(self, label='', template='hemlock/option.html', **kwargs):
        super().__init__(label, template, **kwargs)

    @property
    def label(self):
        return self.body.text('option')
    
    @label.setter
    def label(self, val):
        self.body.set_element('option', val)

    def click(self, driver, if_selected=None):
        """
        Use a selenium webdriver to click on this choice.

        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver
            The selenium webdriver that clicks this choice. Does not have to 
            be chromedriver.

        if_selected : bool or None, default=None
            Indicates that the choice will be clicked only if it is already 
            selected. If `False` the choice will be clicked only if it is not 
            already selected. If `None` the choice will be clicked whether or 
            not it is selected.

        Returns
        -------
        self
        """
        option = driver.find_element_by_css_selector('#'+self.id)
        if (
            if_selected is None 
            or if_selected == bool(option.get_attribute('selected'))
        ):
            option.click()
        return self

    def is_displayed(self, driver):
        """
        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver
            The selenium webdriver that clicks this choice. Does not have to 
            be chromedriver.

        Returns
        -------
        is_displayed : bool
            Indicates that this choice is visible in the browser.
        """
        option = driver.find_element_by_css_selector('#'+self.id)
        return option.is_displayed()
    
    def _render(self, question, idx, body=None):
        """Render the choice HTML
        
        Parameters
        ----------
        question : hemlock.Question
            Question to which this choice belongs.

        idx : int
            Index of this choice in the question's `choices` list.
        """
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