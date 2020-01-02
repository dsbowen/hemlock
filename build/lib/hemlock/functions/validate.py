"""Response validation

This file specifies the following types of validation:
1. Require and type
2. Set (response is or is not in a set)
3. Value
4. Number of characters or selected choices
5. Number of words
6. Number of decimals
7. Regex
8. Correct choice (choice value evaluates to True)

For value and number of xxx validation, programmers can set the minimum 
value, the maximum value, the range of accepted values, or the exact value.

For example, if you want a dollar amount to the cent, use the 
`exact_decimals` function with a `value` of 2.
"""

from hemlock.database import Validate
from hemlock.functions.utils import _correct_choices

from operator import __ge__, __le__
import re

"""Utils"""

def indef_article(string):
    return 'an ' if string[0] in 'aeiou' else 'a '

def plural(val):
    return '' if val == 1 else 's'

"""Require and type validation"""

@Validate.register
def require(question, error_msg=None):
    if not question.response:
        return error_msg or '<p>Please respond to this question.<p>'

@Validate.register
def is_type(question, resp_type, type_name=None, error_msg=None):
    """Validate that the response can be converted to a given type"""
    try:
        resp_type(question.response)
        return
    except:
        pass
    if error_msg is not None:
        return error_msg
    if type_name is None:
        if resp_type == int:
            type_name = 'integer'
        elif resp_type == float:
            type_name = 'number'
    if type_name is not None:
        type_name = indef_article(type_name) + type_name
    else:
        type_name = 'the correct type of response'
    return '<p>Please enter {}.</p>'.format(type_name)

"""Set validation"""

IS_IN_MSG = '<p>Please enter one of the following: {}.</p>'

@Validate.register
def is_in(question, valid_set, resp_type=None, error_msg=None):
    if _convert_resp(question.response, resp_type) not in valid_set:
        s = ', '.join([str(s) for s in valid_set])
        return error_msg or IS_IN_MSG.format(s)

IS_NOT_IN = '<p>Please do not enter any of the following: {}.</p>'

@Validate.register
def is_not_in(question, invalid_set, resp_type=None, error_msg=None):
    if _convert_resp(question.response, resp_type) in invalid_set:
        s = ', '.join([str(s) for s in invalid_set])
        return error_msg or IS_NOT_IN.format(s)

def _convert_resp(resp, resp_type):
    return resp if resp_type is None else resp_type(resp)

"""Range validation

`resp_type` specifies the type into which the participant's response is 
converted for comparison against a min or max value. If none is specified, 
these methods assume the response type is that of the min or max value.
"""

MAX_MSG = '<p>Please enter a response less than {}.</p>'

@Validate.register
def max_val(question, max, resp_type=None, error_msg=None):
    error_msg = error_msg or MAX_MSG.format(max)
    return _in_range(question, max, resp_type, error_msg, __le__)

MIN_MSG = '<p>Please enter a response greater than {}.</p>'

@Validate.register
def min_val(question, min, resp_type=None, error_msg=None):
    error_msg = error_msg or MIN_MSG.format(min)
    return _in_range(question, min, resp_type, error_msg, __ge__)

def _in_range(question, val, resp_type, error_msg, comparator):
    resp_type = resp_type or type(val)
    type_error_msg = is_type(question, resp_type)
    if type_error_msg is not None:
        return type_error_msg or error_msg
    if not comparator(resp_type(question.response), val):
        return error_msg

RANGE_MSG = '<p>Please enter a response between {min} and {max}.</p>'

@Validate.register
def range_val(question, min, max, resp_type=None, error_msg=None):
    if resp_type is None:
        assert type(min) == type(max)
        resp_type = type(min)
    type_error_msg = is_type(question, resp_type)
    if type_error_msg is not None:
        return error_msg or type_error_msg
    if not (min <= resp_type(question.response) <= max):
        return error_msg or RANGE_MSG.format(min=min, max=max)

"""Length validation

Note that length validation applies to the length of a string response, or 
the number of selected choices for a `ChoiceQuestion`. This is because 
`response` stores a list of selected choices.
"""

MAX_CHOICES_MSG = '<p>Please select at most {0} choice{1}.</p>'
MAX_LEN_MSG = '<p>Please enter a response at most {0} character{1} long.</p>'

@Validate.register
def max_len(question, max, error_msg=None):
    """
    Note that a response of None satisfies all max length validation.
    """
    if not question.response:
        return
    if len(question.response) <= max:
        return
    if error_msg is not None:
        return error_msg
    if isinstance(question.response, list):
        return MAX_CHOICES_MSG.format(max, plural(max))
    return MAX_LEN_MSG.format(max, plural(max))

MIN_CHOICES_MSG = '<p>Please select at least {0} choice{1}.</p>'
MIN_LEN_MSG = '<p>Please enter a response at least {0} character{1} long.</p>'

@Validate.register
def min_len(question, min, error_msg=None):
    msg = require(question)
    if min and msg is not None:
        return error_msg or msg
    if min <= len(question.response):
        return
    if error_msg is not None:
        return error_msg
    if isinstance(question.response, list):
        return MIN_CHOICES_MSG.format(min, plural(min))
    return MIN_LEN_MSG.format(min, plural(min))

NUM_CHOICES_RANGE_MSG = '<p>Please select between {0} and {1} choices.</p>'
RANGE_LEN_MSG = '<p>Please enter a response {0} to {1} characters long.</p>'

@Validate.register
def range_len(question, min, max, error_msg=None):
    msg = require(question)
    if min and msg is not None:
        return error_msg or msg
    if min <= len(question.response) <= max:
        return
    if error_msg is not None:
        return error_msg
    if isinstance(question.response, list):
        return NUM_CHOICES_RANGE_MSG.format(min, max)
    return RANGE_LEN_MSG.format(min, max)

NUM_CHOICES_EXACT_MSG = '<p>Please select exactly {0} choice{1}.</p>'
EXACT_LEN_MSG = '<p>Please enter a response exactly {0} character{1} long.</p>'

@Validate.register
def exact_len(question, value, error_msg=None):
    msg = require(question)
    if value and msg is not None:
        return error_msg or msg
    if len(question.response) == value:
        return
    if error_msg is not None:
        return error_msg
    if isinstance(question.response, list):
        return NUM_CHOICES_EXACT_MSG.format(value, plural(value))
    return EXACT_LEN_MSG.format(value, plural(value))

"""Number of words"""

MAX_WORDS_MSG = '<p>Please enter a response at most {0} word{1} long.</p>'

@Validate.register
def max_words(question, max, error_msg=None):
    if not question.response:
        return
    assert isinstance(question.response, str)
    if num_words(question.response) > max:
        return error_msg or MAX_WORDS_MSG.format(max, plural(max))

MIN_WORDS_MSG = '<p>Please enter a response at least {0} word{1} long.</p>'

@Validate.register
def min_words(question, min, error_msg=None):
    msg = require(question)
    if min and msg is not None:
        return error_msg or msg
    assert isinstance(question.response, str)
    if num_words(question.response) < min:
        return error_msg or MIN_WORDS_MSG.format(min, plural(min))

RANGE_WORDS_MSG = '<p>Please enter a response {0} to {1} words long.</p>'

@Validate.register
def range_words(question, min, max, error_msg=None):
    msg = require(question)
    if min and msg is not None:
        return error_msg or msg 
    assert isinstance(question.response, str)
    if not (min <= num_words(question.response) <= max):
        return error_msg or RANGE_WORDS_MSG.format(min, max)

EXACT_WORDS_MSG = '<p>Please enter a response exactly {0} word{1} long.</p>'

@Validate.register
def exact_words(question, value, error_msg=None):
    """
    Note that a response of None can satisfy exact_words if `value`==0.
    """
    msg = require(question)
    if value and msg is not None:
        return error_msg or msg
    assert isinstance(question.response, str)
    if not num_words(question.response) == value:
        return error_msg or EXACT_WORDS_MSG.format(value, plural(value))

@Validate.register
def num_words(string):
    """Count the number of words in the string"""
    return len(re.findall(r'\w+', string))

"""Decimal validation"""

MAX_DECIMALS = '<p>Please enter a number with at most {0} decimal{1}.</p>'

@Validate.register
def max_decimals(question, max, error_msg=None):
    msg, decimals = _get_decimals(question, error_msg)
    if msg:
        return msg
    if decimals > max:
        return error_msg or MAX_DECIMALS.format(max, plural(max))

MIN_DECIMALS = '<p>Please enter a number with at least {0} decimal{1}.</p>'

@Validate.register
def min_decimals(question, min, error_msg=None):
    msg, decimals = _get_decimals(question, error_msg)
    if msg:
        return msg
    if decimals < min:
        return error_msg or MIN_DECIMALS.format(min, plural(min))

RANGE_DECIMALS = '<p>Please enter a number with {0} to {1} decimals.</p>'

@Validate.register
def range_decimals(question, min, max, error_msg=None):
    msg, decimals = _get_decimals(question, error_msg)
    if msg:
        return msg
    if not (min <= decimals <= max):
        return RANGE_DECIMALS.format(min, max)

EXACT_DECIMALS = '<p>Please enter a number with exactly {0} decimal{1}.</p>'

@Validate.register
def exact_decimals(question, value, error_msg=None):
    msg, decimals = _get_decimals(question, error_msg)
    if msg:
        return msg
    if not decimals == value:
        return EXACT_DECIMALS.format(value, plural(value))

def _get_decimals(question, error_msg):
    """Return (error message, number of decimals) tuple

    This validation will fail if the response cannot be converted to `float`.
    """
    msg = is_type(question, float)
    if msg:
        return error_msg or msg, None
    split = question.response.split('.')
    # Number of decimals is 0 when no decimal point is specified.
    decimals = 0 if len(split) == 1 else len(split[-1])
    return None, decimals

"""Regex"""

REGEX_MSG = '<p>Please enter a response with the correct pattern.</p>'

@Validate.register
def match(question, pattern, error_msg=None):
    """Validate that the response matches the regex pattern."""
    if not re.compile(pattern).match((question.response or '')):
        return error_msg or REGEX_MSG

"""Choice validation"""

@Validate.register
def correct_choices(question, error_msg=None):
    """Validate that selected choice(s) is (are) correct"""
    if not _correct_choices(question):
        if error_msg is not None:
            return error_msg
        if question.multiple:
            return '<p>Please select the correct choice(s).</p>'
        if len([c for c in question.choices if c.value]) == 1:
            return '<p>Please select the correct choice.</p>'
        return '<p>Please select one of the correct choices.</p>'