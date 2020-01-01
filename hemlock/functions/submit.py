"""Submit functions"""

from hemlock.app import Settings
from hemlock.database import Submit
from hemlock.functions.utils import _correct_choices

from flask import current_app

import re

@Submit.register
def data_type(question, new_type, *args, **kwargs):
    """Convert the data to a new type"""
    question.data = new_type(question.data, *args, **kwargs)

@Submit.register
def match(question, pattern):
    """
    Convert the data to a 0-1 indicator that the data matches the pattern.
    """
    question.data = int(re.match(pattern, (question.data or '')) is not None)

@Submit.register
def correct_choices(question):
    """
    Convert the data to a 0-1 indicator that the participant selected the 
    correct choices.
    """
    question.data = int(_correct_choices(question))