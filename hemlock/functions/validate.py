"""# Validation functions

These are built-in functions to validate a participant's response to a 
question. They return `None` if the response is valid, and an error message if 
the repsonse is invalid.

You can input a custom error message for any of these functions with the 
`error_msg` argument.
"""

from ..models import Validate
from ..tools.lang import indef_article, plural
from .utils import convert, correct_choices 

import re
from operator import __ge__, __le__

# Require and type validation

IS_TYPE_MSG = '<p>Please enter {}.</p>'

@Validate.register
def is_type(question, resp_type, error_msg=None):
    """
    Validate that the response can be converted to a given type.
    
    Parameters
    ----------
    question : hemlock.Question

    resp_type : class
        The required type of response.
    """
    try:
        resp_type(question.response)
        return
    except:
        pass
    if error_msg is not None:
        return error_msg
    if resp_type == int:
        return IS_TYPE_MSG.format('an integer')
    if resp_type == float:
        return IS_TYPE_MSG.format('a number')
    return IS_TYPE_MSG.format('the correct type of response')

REQUIRE_MSG = '<p>Please respond to this question.<p>'

@Validate.register
def require(question, error_msg=None):
    """
    Require a response to this question.

    Parameters
    ----------
    question : hemlock.Question
    """
    if not question.response:
        return error_msg or REQUIRE_MSG

# Set validation

IS_IN_MSG = '<p>Please enter one of the following: {}.</p>'

@Validate.register
def is_in(question, valid_set, resp_type=None, error_msg=None):
    """
    Validate that the question response is in a set of valid responses.

    Parameters
    ----------
    question : hemlock.Question
    
    valid_set : iterable
        Set of valid responses.

    resp_type : class or None, default=None
        Type of response expected; should match the type of elements in 
        `valid_set`.
    """
    resp, _ = convert(question.response, resp_type)
    if resp not in valid_set:
        if error_msg is not None:
            return error_msg
        return IS_IN_MSG.format(', '.join([str(i) for i in valid_set]))

NOT_IN_MSG = '<p>Please do not enter any of the following: {}.</p>'

@Validate.register
def is_not_in(question, invalid_set, resp_type=None, error_msg=None):
    """
    Validate that the question response is *not* in a set of invalid 
    responses.

    Parameters
    ----------
    question : hemlock.Question

    invalid_set : iterable
        Set of invalid responses.

    resp_type : class or None, default=None
        Type of response expected; should match the type of elements in
        `invalid_set`.
    """
    resp, _ = convert(question.response, resp_type)
    if resp in invalid_set:
        if error_msg is not None:
            return error_msg
        return NOT_IN_MSG.format(', '.join([str(i) for i in invalid_set]))

# Range validation

MAX_MSG = '<p>Please enter a response less than {}.</p>'

@Validate.register
def max_val(question, max, resp_type=None, error_msg=None):
    error_msg = error_msg or MAX_MSG.format(max)
    return _compare_resp(question, max, resp_type, error_msg, __le__)

MIN_MSG = '<p>Please enter a response greater than {}.</p>'

@Validate.register
def min_val(question, min, resp_type=None, error_msg=None):
    error_msg = error_msg or MIN_MSG.format(min)
    return _compare_resp(question, min, resp_type, error_msg, __ge__)

def _compare_resp(question, val, comparator, error_msg, resp_type=None):
    """
    Compare question response.

    Parameters
    ----------
    question : hemlock.Question

    val :
        Comparison value.

    comparator : callable
        Takes `question.resposne` and `val` and returns a bool indicating that 
        the comparison was 'successful'.

    error_msg : str
        Error message to be displayed if comparison is unsuccessful.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the type of `val` will be used.
    """
    resp_type = resp_type or type(val)
    type_error_msg = is_type(question, resp_type)
    if type_error_msg is not None:
        return type_error_msg
    if not comparator(resp_type(question.response), val):
        return error_msg

RANGE_MSG = '<p>Please enter a response between {0} and {1}.</p>'

@Validate.register
def range_val(question, min, max, resp_type=None, error_msg=None):
    """
    Validate that the response is in a given range.

    Parameters
    ----------
    question : hemlock.Question
    
    min : 
        Minimum value for the question response.

    max :
        Maximum value for the question response.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the expected response type is the type of `min` and `max`, which must be of the same type.
    """
    if resp_type is None:
        assert type(min) == type(max)
        resp_type = type(min)
    type_error_msg = is_type(question, resp_type)
    if type_error_msg is not None:
        return type_error_msg
    if not (min <= resp_type(question.response) <= max):
        return error_msg or RANGE_MSG.format(min, max)

# Length validation

EXACT_CHOICES_MSG = '<p>Please select exactly {0} {choice}.</p>'
EXACT_LEN_MSG = '<p>Please enter a response exactly {0} {character} long.</p>'

@Validate.register
def exact_len(question, len_, error_msg=None):
    """
    Validates the exact length of the repsonse. For a string response, this is 
    the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question

    len_ : int
        Required length of the response.
    """
    msg = require(question)
    if len_ and msg is not None:
        return error_msg or msg
    if len(question.response) == len_:
        return
    if error_msg is not None:
        return error_msg
    if isinstance(question.response, list):
        return EXACT_CHOICES_MSG.format(len_, choice=plural(len_, 'choice'))
    return EXACT_LEN_MSG.format(len_, character=plural(len_, 'character'))

MAX_CHOICES_MSG = '<p>Please select at most {0} {choice}.</p>'
MAX_LEN_MSG = '<p>Please enter a response at most {0} {character} long.</p>'

@Validate.register
def max_len(question, max, error_msg=None):
    """
    Validates the maximum length of the response. For a string response, this 
    is the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question

    max : int
        Maximum length of the response.

    Notes
    -----
    A response of `None` is assumed to satisfy the max length validation. Use 
    `Validate.require` to require a response that is not `None`.
    """
    if not question.response:
        return
    if len(question.response) <= max:
        return
    if error_msg is not None:
        return error_msg
    if isinstance(question.response, list):
        return MAX_CHOICES_MSG.format(max, choice=plural(max, 'choice'))
    return MAX_LEN_MSG.format(max, character=plural(max, 'character'))

MIN_CHOICES_MSG = '<p>Please select at least {0} choice{1}.</p>'
MIN_LEN_MSG = '<p>Please enter a response at least {0} character{1} long.</p>'

@Validate.register
def min_len(question, min, error_msg=None):
    """
    Valiadates the minimum length of the response. For a string response, this 
    is the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question
    
    min : int
        Minimum length of the response.
    """
    msg = require(question)
    if min and msg is not None:
        return error_msg or msg
    if min <= len(question.response):
        return
    if error_msg is not None:
        return error_msg
    if isinstance(question.response, list):
        return MIN_CHOICES_MSG.format(min, choice=plural(min, 'choice'))
    return MIN_LEN_MSG.format(min, character=plural(min, 'character'))

RANGE_CHOICES_MSG = '<p>Please select between {0} and {1} choices.</p>'
RANGE_LEN_MSG = '<p>Please enter a response {0} to {1} characters long.</p>'

@Validate.register
def range_len(question, min, max, error_msg=None):
    """
    Validates the range of the response length. For a string response, this is 
    the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question

    min : int
        Minimum response length.

    max : int
        Maximum response length.
    """
    msg = require(question)
    if min and msg is not None:
        return error_msg or msg
    if min <= len(question.response) <= max:
        return
    if error_msg is not None:
        return error_msg
    if isinstance(question.response, list):
        return RANGE_CHOICES_MSG.format(min, max)
    return RANGE_LEN_MSG.format(min, max)

# Words validation

EXACT_WORDS_MSG = '<p>Please enter a response exactly {0} {word} long.</p>'

@Validate.register
def exact_words(question, nwords, error_msg=None):
    """
    Validate the exact number of words in the response.

    Parameters
    ----------
    question : hemlock.Question
    
    nwords : int
        Required number of words.
    """
    msg = require(question)
    if value and msg is not None:
        # a response of `None` can satisfy `exact_words` if `value==0`
        return error_msg or msg
    assert isinstance(question.response, str)
    if _num_words(question.response) != nwords:
        return (
            error_msg 
            or EXACT_WORDS_MSG.format(nwords, word=plural(nwords, 'word'))
        )

MAX_WORDS_MSG = '<p>Please enter at most {0} {word}.</p>'

@Validate.register
def max_words(question, max, error_msg=None):
    """
    Validates the maximum number of words in the response.

    Parameters
    ----------
    question : hemlock.Question

    max : int
        Maximum number of words.
    """
    if not question.response:
        return
    assert isinstance(question.response, str)
    if _num_words(question.response) > max:
        return error_msg or MAX_WORDS_MSG.format(max, word=plural(max,'word'))

MIN_WORDS_MSG = '<p>Please enter at least {0} {word}.</p>'

@Validate.register
def min_words(question, min, error_msg=None):
    """
    Validates the minimum number of words in the repsonse.

    Parameters
    ----------
    question : hemlock.Question

    min : int
        Minimum number of words.
    """
    msg = require(question)
    if min and msg is not None:
        return error_msg or msg
    assert isinstance(question.response, str)
    if _num_words(question.response) < min:
        return error_msg or MIN_WORDS_MSG.format(min, word=plural(min,'word'))

RANGE_WORDS_MSG = '<p>Please enter between {0} and {1} words.</p>'

@Validate.register
def range_words(question, min, max, error_msg=None):
    """
    Validates the number of words falls in a given range.

    Parameters
    ----------
    question : hemlock.Question

    min : int
        Minumum number of words.

    max : int
        Maximum number of words.
    """
    msg = require(question)
    if min and msg is not None:
        return error_msg or msg 
    assert isinstance(question.response, str)
    if not (min <= _num_words(question.response) <= max):
        return error_msg or RANGE_WORDS_MSG.format(min, max)

def _num_words(string):
    """Count the number of words in the string"""
    return len(re.findall(r'\w+', string))

# Decimal validation

EXACT_DECIMALS = '<p>Please enter a number with exactly {0} {decimal}.</p>'

@Validate.register
def exact_decimals(question, ndec, error_msg=None):
    """
    Validates the exact number of decimals.

    Parameters
    ----------
    question : hemlock.Question

    ndec : int
        Required number of decimals.
    """
    msg, decimals = _get_decimals(question, error_msg)
    if msg:
        return msg
    if decimals != ndec:
        return EXACT_DECIMALS.format(ndec, decimal=plural(ndec, 'decimal'))

MAX_DECIMALS = '<p>Please enter a number with at most {0} {decimal}.</p>'

@Validate.register
def max_decimals(question, max, error_msg=None):
    """
    Validates the maximum number of decimals.

    Parameters
    ----------
    question : hemlock.Question

    max : int
        Maximum number of decimals.
    """
    msg, decimals = _get_decimals(question, error_msg)
    if msg:
        return msg
    if decimals > max:
        return (
            error_msg 
            or MAX_DECIMALS.format(max, decimal=plural(max, 'decimal'))
        )

MIN_DECIMALS = '<p>Please enter a number with at least {0} {decimal}.</p>'

@Validate.register
def min_decimals(question, min, error_msg=None):
    """
    Validates the minumum number of decimals.

    Parameters
    ----------
    question : hemlock.Question

    min : int
        Minumum number of decimals.
    """
    msg, decimals = _get_decimals(question, error_msg)
    if msg:
        return msg
    if decimals < min:
        return (
            error_msg 
            or MIN_DECIMALS.format(min, decimal=plural(min, 'decimal'))
        )

RANGE_DECIMALS = '<p>Please enter a number with {0} to {1} decimals.</p>'

@Validate.register
def range_decimals(question, min, max, error_msg=None):
    """
    Validates the number of decimals are in a given range.

    Parameters
    ----------
    question : hemlock.Question
    
    min : int
        Minimum number of decimals.

    max : int
        Maximum number of decimals.
    """
    msg, decimals = _get_decimals(question, error_msg)
    if msg:
        return msg
    if not (min <= decimals <= max):
        return RANGE_DECIMALS.format(min, max)

def _get_decimals(question, error_msg):
    """Return (error message, number of decimals) tuple

    This validation will fail if the response cannot be converted to `float`.
    """
    msg = is_type(question, float)
    if msg:
        return error_msg or msg, None
    split = question.response.split('.')
    # number of decimals is 0 when no decimal point is specified.
    decimals = 0 if len(split) == 1 else len(split[-1])
    return None, decimals

# Regex validation

REGEX_MSG = '<p>Please enter a response with the correct pattern.</p>'

@Validate.register
def match(question, pattern, error_msg=None):
    """
    Validate that the response matches the regex pattern.
    
    Parameters
    ----------
    question : hemlock.Question

    pattern : str
        Regex pattern to match.
    """
    if not re.compile(pattern).match((question.response or '')):
        return error_msg or REGEX_MSG

# Choice validation

@Validate.register
def correct_choices(question, *correct, error_msg=None):
    """
    Validate that selected choice(s) is correct.
    
    Parameters
    ----------
    question : hemlock.Question

    \*correct :
        Correct choices.
    """
    if not correct_choices(question, *correct):
        if error_msg is not None:
            return error_msg
        if question.multiple:
            return '<p>Please select the correct choice(s).</p>'
        if len([c for c in question.choices if c.value]) == 1:
            return '<p>Please select the correct choice.</p>'
        return '<p>Please select one of the correct choices.</p>'