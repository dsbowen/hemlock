"""# Validation functions

These are built-in functions to validate a participant's response to a 
question. They return `None` if the response is valid, and an error message if 
the repsonse is invalid.
"""

from ..models import Validate
from ..tools.lang import join, plural
from .utils import convert, correct_choices as correct_choices_

import re
from operator import __ge__, __le__

# Require and type validation

RESP_TYPE_MSG = '<p>Please enter {}.</p>'

@Validate.register
def response_type(question, resp_type):
    """
    Validate that the response can be converted to a given type.
    
    Parameters
    ----------
    question : hemlock.Question

    resp_type : class
        The required type of response.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.response_type(Input(response='hello world'), float)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number.
    ```
    """
    try:
        resp_type(question.response)
        return
    except:
        if resp_type == int:
            return RESP_TYPE_MSG.format('an integer')
        if resp_type == float:
            return RESP_TYPE_MSG.format('a number')
        return RESP_TYPE_MSG.format('the correct type of response')

REQUIRE_MSG = '<p>Please respond to this question.<p>'

@Validate.register
def require(question):
    """
    Require a response to this question.

    Parameters
    ----------
    question : hemlock.Question

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.require(Input(response=None))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please respond to this question.
    ```
    """
    return None if question.response else REQUIRE_MSG

# Set validation

IS_IN_MSG = '<p>Please enter {}.</p>'

@Validate.register
def is_in(question, valid_set, resp_type=None):
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

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.is_in(Input(response='earth'), ('wind', 'fire'))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter wind or fire.
    ```
    """
    resp, _ = convert(question.response, resp_type)
    if resp not in valid_set:
        return IS_IN_MSG.format(join('or', *valid_set))

NOT_IN_MSG = '<p>Please do not enter {}.</p>'

@Validate.register
def is_not_in(question, invalid_set, resp_type=None):
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

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.is_not_in(
    \    Input(response='earth'), ('earth','wind','fire')
    )
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please do not enter earth, wind, or fire.
    ```
    """
    resp, _ = convert(question.response, resp_type)
    if resp in invalid_set:
        return NOT_IN_MSG.format(join('or', *invalid_set))

# Range validation

MAX_MSG = '<p>Please enter a response less than {}.</p>'

@Validate.register
def max_val(question, max_, resp_type=None):
    """
    Validate that the response does not exceed a maximum value.

    Parameters
    ----------
    question : hemlock.Question

    max_ : 
        Maximum value.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the type of `max` will be used.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.max_val(Input(response='101'), 100)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a response less than 100.
    ```
    """
    error_msg = MAX_MSG.format(max_)
    return _compare_resp(question, max_, __le__, error_msg, resp_type)

MIN_MSG = '<p>Please enter a response greater than {}.</p>'

@Validate.register
def min_val(question, min_, resp_type=None):
    """
    Validate that the response does not deceed a minumum value.

    Parameters
    ----------
    question : hemlock.Question

    min_ : 
        Minimum value.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the type of `min` will be used.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.min_val(Input(response='-1'), 0)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a response greater than 0.
    ```
    """
    error_msg = MIN_MSG.format(min_)
    return _compare_resp(question, min_, __ge__, error_msg, resp_type)

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
    type_error_msg = response_type(question, resp_type)
    if type_error_msg is not None:
        return type_error_msg
    if not comparator(resp_type(question.response), val):
        return error_msg

RANGE_MSG = '<p>Please enter a response between {0} and {1}.</p>'

@Validate.register
def range_val(question, min_, max_, resp_type=None):
    """
    Validate that the response is in a given range.

    Parameters
    ----------
    question : hemlock.Question
    
    min_ : 
        Minimum value for the question response.

    max_ :
        Maximum value for the question response.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the expected response type is 
        the type of `min` and `max`, which must be of the same type.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.range_val(Input(response='101'), 0, 100)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a response between 0 and 100.
    ```
    """
    if resp_type is None:
        assert type(min_) == type(max_)
        resp_type = type(min_)
    type_error_msg = response_type(question, resp_type)
    if type_error_msg is not None:
        return type_error_msg
    if not (min_ <= resp_type(question.response) <= max_):
        return RANGE_MSG.format(min_, max_)

# Length validation

EXACT_CHOICES_MSG = '<p>Please select exactly {0} {choice}.</p>'
EXACT_LEN_MSG = '<p>Please enter exactly {0} {character}.</p>'

@Validate.register
def exact_len(question, len_):
    """
    Validates the exact length of the repsonse. For a string response, this is 
    the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question

    len_ : int
        Required length of the response.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.exact_len(Input(response='hello world'), 5)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter exactly 5 characters.
    ```
    """
    msg = require(question)
    if len_ and msg is not None:
        return msg
    if len(question.response) == len_:
        return
    if isinstance(question.response, list):
        return EXACT_CHOICES_MSG.format(len_, choice=plural(len_, 'choice'))
    return EXACT_LEN_MSG.format(len_, character=plural(len_, 'character'))

MAX_CHOICES_MSG = '<p>Please select at most {0} {choice}.</p>'
MAX_LEN_MSG = '<p>Please enter at most {0} {character}.</p>'

@Validate.register
def max_len(question, max_):
    """
    Validates the maximum length of the response. For a string response, this 
    is the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question

    max_ : int
        Maximum length of the response.

    Notes
    -----
    A response of `None` is assumed to satisfy the max length validation. Use 
    `Validate.require` to require a response that is not `None`.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.max_val(Input(response='hello world'), 5)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter at most 5 characters.
    ```
    """
    if not question.response:
        return
    if len(question.response) <= max_:
        return
    if isinstance(question.response, list):
        return MAX_CHOICES_MSG.format(max_, choice=plural(max_, 'choice'))
    return MAX_LEN_MSG.format(max_, character=plural(max_, 'character'))

MIN_CHOICES_MSG = '<p>Please select at least {0} {choice}.</p>'
MIN_LEN_MSG = '<p>Please enter at least {0} {character}.</p>'

@Validate.register
def min_len(question, min_):
    """
    Valiadates the minimum length of the response. For a string response, this 
    is the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question
    
    min_ : int
        Minimum length of the response.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.min_len(Input(response='hello world'), 15)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter at least 15 characters.
    ```
    """
    if min_ <= 0:
        return
    msg = require(question)
    if msg is not None:
        return msg
    if min_ <= len(question.response):
        return
    if isinstance(question.response, list):
        return MIN_CHOICES_MSG.format(min_, choice=plural(min_, 'choice'))
    return MIN_LEN_MSG.format(min_, character=plural(min_, 'character'))

RANGE_CHOICES_MSG = '<p>Please select between {0} and {1} choices.</p>'
RANGE_LEN_MSG = '<p>Please enter between {0} and {1} characters.</p>'

@Validate.register
def range_len(question, min_, max_):
    """
    Validates the range of the response length. For a string response, this is 
    the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question

    min_ : int
        Minimum response length.

    max_ : int
        Maximum response length.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.range_len(Input(response='hello world'), 5, 10)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter 5 to 10 characters.
    ```
    """
    if min_ <= 0:
        return
    msg = require(question)
    if msg is not None:
        return msg
    if min_ <= len(question.response) <= max_:
        return
    if isinstance(question.response, list):
        return RANGE_CHOICES_MSG.format(min_, max_)
    return RANGE_LEN_MSG.format(min_, max_)

# Words validation

EXACT_WORDS_MSG = '<p>Please enter exactly {0} {word}.</p>'

@Validate.register
def exact_words(question, nwords):
    """
    Validate the exact number of words in the response.

    Parameters
    ----------
    question : hemlock.Question
    
    nwords : int
        Required number of words.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.exact_words(Input(response='hello world'), 1)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter exactly 1 word.
    ```
    """
    msg = require(question)
    if nwords and msg is not None:
        # a response of `None` can satisfy `exact_words` if `value==0`
        return msg
    assert isinstance(question.response, str)
    if _num_words(question.response) != nwords:
        return EXACT_WORDS_MSG.format(nwords, word=plural(nwords, 'word'))

MAX_WORDS_MSG = '<p>Please enter at most {0} {word}.</p>'

@Validate.register
def max_words(question, max_):
    """
    Validates the maximum number of words in the response.

    Parameters
    ----------
    question : hemlock.Question

    max_ : int
        Maximum number of words.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.max_words(Input(response='hello world'), 1)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter at most 1 word.
    ```
    """
    if not question.response:
        return
    assert isinstance(question.response, str)
    if _num_words(question.response) > max_:
        return MAX_WORDS_MSG.format(max_, word=plural(max_,'word'))

MIN_WORDS_MSG = '<p>Please enter at least {0} {word}.</p>'

@Validate.register
def min_words(question, min_):
    """
    Validates the minimum number of words in the repsonse.

    Parameters
    ----------
    question : hemlock.Question

    min_ : int
        Minimum number of words.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.min_words(Input(response='hello world'), 3)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter at least 3 words.
    ```
    """
    if min_ <= 0:
        return
    msg = require(question)
    if msg is not None:
        return msg
    assert isinstance(question.response, str)
    if _num_words(question.response) < min_:
        return MIN_WORDS_MSG.format(min_, word=plural(min_,'word'))

RANGE_WORDS_MSG = '<p>Please enter between {0} and {1} words.</p>'

@Validate.register
def range_words(question, min_, max_):
    """
    Validates the number of words falls in a given range.

    Parameters
    ----------
    question : hemlock.Question

    min_ : int
        Minumum number of words.

    max_ : int
        Maximum number of words.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.range_words(Input(response='hello world'), 3, 5)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter between 3 and 5 words.
    ```
    """
    if min_ <= 0:
        return
    msg = require(question)
    if msg is not None:
        return msg 
    assert isinstance(question.response, str)
    if not (min_ <= _num_words(question.response) <= max_):
        return RANGE_WORDS_MSG.format(min_, max_)

def _num_words(string):
    """Count the number of words in the string"""
    return len(re.findall(r'\w+', string))

# Decimal validation

EXACT_DECIMALS = '<p>Please enter a number with exactly {0} {decimal}.</p>'

@Validate.register
def exact_decimals(question, ndec):
    """
    Validates the exact number of decimals.

    Parameters
    ----------
    question : hemlock.Question

    ndec : int
        Required number of decimals.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.exact_decimals(Input(response='1'), 2)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number with exactly 2 decimals.
    ```
    """
    msg, decimals = _get_decimals(question)
    if msg:
        return msg
    if decimals != ndec:
        return EXACT_DECIMALS.format(ndec, decimal=plural(ndec, 'decimal'))

MAX_DECIMALS = '<p>Please enter a number with at most {0} {decimal}.</p>'

@Validate.register
def max_decimals(question, max_):
    """
    Validates the maximum number of decimals.

    Parameters
    ----------
    question : hemlock.Question

    max_ : int
        Maximum number of decimals.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.max_decimals(Input(response='1.123'), 2)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number with at most 2 decimals.
    ```
    """
    msg, decimals = _get_decimals(question)
    if msg:
        return msg
    if decimals > max_:
        return MAX_DECIMALS.format(max_, decimal=plural(max_, 'decimal'))

MIN_DECIMALS = '<p>Please enter a number with at least {0} {decimal}.</p>'

@Validate.register
def min_decimals(question, min_):
    """
    Validates the minumum number of decimals.

    Parameters
    ----------
    question : hemlock.Question

    min_ : int
        Minumum number of decimals.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.min_decimals(Input(response='1'), 2)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number with at least 2 decimals.
    ```
    """
    msg, decimals = _get_decimals(question)
    if msg:
        return msg
    if decimals < min_:
        return MIN_DECIMALS.format(min_, decimal=plural(min_, 'decimal'))

RANGE_DECIMALS = '<p>Please enter a number with {0} to {1} decimals.</p>'

@Validate.register
def range_decimals(question, min_, max_):
    """
    Validates the number of decimals are in a given range.

    Parameters
    ----------
    question : hemlock.Question
    
    min_ : int
        Minimum number of decimals.

    max_ : int
        Maximum number of decimals.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.range_decimals(Input(response='1.123'), 0, 2)
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number with 0 to 2 decimals.
    ```
    """
    msg, decimals = _get_decimals(question)
    if msg:
        return msg
    if not (min_ <= decimals <= max_):
        return RANGE_DECIMALS.format(min_, max_)

def _get_decimals(question):
    """Return (error message, number of decimals) tuple

    This validation will fail if the response cannot be converted to `float`.
    """
    msg = response_type(question, float)
    if msg:
        return msg, None
    split = question.response.split('.')
    # number of decimals is 0 when no decimal point is specified.
    decimals = 0 if len(split) == 1 else len(split[-1])
    return None, decimals

# Regex validation

REGEX_MSG = '<p>Please enter a response with the correct pattern.</p>'

@Validate.register
def match(question, pattern):
    """
    Validate that the response matches the regex pattern.
    
    Parameters
    ----------
    question : hemlock.Question

    pattern : str
        Regex pattern to match.

    Examples
    --------
    ```python
    from hemlock import Input, Validate, push_app_context

    push_app_context()

    inpt = Validate.match(Input(response='hello world'), 'goodbye *')
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a response with the correct pattern.
    ```
    """
    if not re.compile(pattern).match((question.response or '')):
        return REGEX_MSG

# Choice validation

@Validate.register
def correct_choices(question, correct):
    """
    Validate that selected choice(s) is correct.
    
    Parameters
    ----------
    question : hemlock.Question

    correct : list of hemlock.Choice
        Correct choices.

    Examples
    --------
    ```python
    from hemlock import Check, Validate, push_app_context

    push_app_context()

    check = Check(choices=['correct','incorrect','also incorrect'])
    Validate.correct_choices(check, [check.choices[0]])
    check.response = check.choices[1]
    check._validate()
    check.error
    ```

    Out:

    ```
    Please select the correct choice.
    ```
    """
    if not correct_choices_(question, correct):
        if question.multiple:
            return '<p>Please select the correct choice(s).</p>'
        if len(correct) == 1:
            return '<p>Please select the correct choice.</p>'
        return '<p>Please select one of the correct choices.</p>'