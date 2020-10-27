"""# Choices and Options

The difference between `hemlock.Choice` and `hemlock.Option` is the former are 
for `hemlock.Check` questions, while latter are for `hemlock.Select` questions.

The use of choice and option models is not due to any deep functional 
difference between them, but reflects the underlying html.
"""

from ..app import db, settings
from ..models import Base
from ..tools import format_attrs, key
from .bases import InputBase

from convert_list import ConvertList
from flask import render_template
from sqlalchemy.types import JSON, TypeDecorator
from sqlalchemy_mutable import MutableList
import json
import time


class ChoiceBase(InputBase, Base):
    """
    Base class for choices.

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Choice label.

    template : str
        Jinja template for the choice html.

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
    key : str
        Randomly generated from ascii letters and digits.

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
    def __init__(self, label=None, **kwargs):
        self.key = key(10)
        self.set_all(label)
        super().__init__(**kwargs)

    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, self.value.__repr__())

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

    def dump(self):
        return json.dumps(self.__dict__)

    @classmethod
    def load(cls, state_dict):
        return cls(**json.loads(state_dict))


class ChoiceListTypeBase(TypeDecorator):
    impl = JSON
    choice_cls = None # must be implemented by ChoiceListType

    def process_bind_param(self, choices, dialect):
        return [choice.dump() for choice in choices]

    def process_result_value(self, state_dicts, dialect):
        return [self.choice_cls.load(state) for state in state_dicts]


class ChoiceListBase(ConvertList, MutableList):
    """
    Converts items in a list of choices to the choice class.
    """
    choice_cls = None # must be implemented by ChoiceList

    @classmethod
    def convert(cls, item):
        if isinstance(item, cls.choice_cls):
            # item is already the choice class
            return item
        if isinstance(item, dict):
            # item is a dict of keyword arguments for the choice class
            return cls.choice_cls(**item)
        if isinstance(item, (tuple, list)):
            if len(item) == 2:
                # item is (label, value) tuple
                return cls.choice_cls(label=item[0], value=item[1])
            if len(item) == 3:
                # item is (label, value, name) tuple
                return cls.choice_cls(
                    label=item[0], value=item[1], name=item[2]
                )
        # item is label, value, name
        return cls.choice_cls(label=str(item), value=item, name=str(item))


settings['Choice'] = dict(
    div_class=['custom-control'], div_attrs={},
    input_attrs={'class': ['custom-control-input']},
    label_attrs={'class': ['custom-control-label', 'w-100', 'choice']}
)

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
    def __init__(self, label=None, template='hemlock/choice.html', **kwargs):
        super().__init__(label, template=template, **kwargs)

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
        inpt = driver.find_element_by_css_selector('#'+self.key)
        if (
            if_selected is None
            or if_selected == bool(inpt.get_attribute('checked'))
        ):
            selector = 'label[for={}]'.format(self.key)
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
        selector = 'label[for={}]'.format(self.key)
        label = driver.find_element_by_css_selector(selector)
        return label.is_displayed()

    def _render(self, question, idx):
        return render_template(
            self.template, c=self, q=question, idx=idx,
            div_attrs=format_attrs(**self.div_attrs),
            input_attrs=format_attrs(**self.input_attrs),
            label_attrs=format_attrs(**self.label_attrs) 
        )

class ChoiceListType(ChoiceListTypeBase):
    choice_cls = Choice

class ChoiceList(ChoiceListBase):
    choice_cls = Choice

ChoiceList.associate_with(ChoiceListType)


settings['Option'] = dict(input_attrs={})

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
    _input_attr_names = ['class', 'disabled']

    def __init__(self, label=None, template='hemlock/option.html', **kwargs):
        super().__init__(label, template=template, **kwargs)

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
        option = driver.find_element_by_css_selector('#'+self.key)
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
        option = driver.find_element_by_css_selector('#'+self.key)
        return option.is_displayed()

    def _render(self, question, idx):
        return render_template(
            self.template, opt=self, q=question, idx=idx, 
            option_attrs=format_attrs(**self.input_attrs)
        )


class OptionListType(ChoiceListTypeBase):
    choice_cls = Option

class OptionList(ChoiceListBase):
    choice_cls = Option

OptionList.associate_with(OptionListType)