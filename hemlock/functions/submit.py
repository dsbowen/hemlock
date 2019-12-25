"""Submit functions"""

from hemlock.database import Submit

import re

@Submit.register
def convert(question, new_type, *args, **kwargs):
    question.data = new_type(question.data, *args, **kwargs)

@Submit.register
def match(question, pattern):
    question.data = int(re.match(pattern, (question.data or '')) is not None)