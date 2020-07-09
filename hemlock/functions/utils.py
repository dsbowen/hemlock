"""Utilities"""

from datetime import MAXYEAR, MINYEAR, datetime, timedelta
from random import randint, random

def convert(obj, type_, *args, **kwargs):
    """
    Converts an object to a new type.

    Parameters
    ----------
    obj :
        Object to convert.

    type_ : class or None
        Desired new type.

    \*args, \*\*kwargs :
        Arguments and keyword arguments to pass to the `type_` constructor.

    Returns
    -------
    obj :
        Converted object, if possible, else original object.

    success : bool
        Indicate that the conversion was successful.
    """
    if type_ is None:
        return obj, True
    try:
        converted = type_(obj, *args, **kwargs)
        return converted, True
    except:
        return obj, False

def correct_choices(q, correct):
    """
    Parameters
    ----------
    q : hemlock.ChoiceQuestion

    correct : list of hemlock.Choice
        Correct choices.

    Returns
    -------
    correct : bool
        Indicates that the participant selected the correct choice(s).

    Notes
    -----
    If the participant can only select one choice, indicate whether the 
    participant selected one of the correct choices.
    """
    resp = q.response.unshell() if isinstance(q.response,list) else q.response
    return set(resp) == set(correct) if q.multiple else resp in correct

def gen_datetime():
    try:
        return datetime(
            randint(MINYEAR, MAXYEAR),
            randint(1,12),
            randint(1,31),
            randint(0,24),
            randint(0,59),
            randint(0,59),
        )
    except:
        return gen_datetime()

def gen_number(mag_lb=0, mag_ub=10, max_decimals=5, p_int=.5, p_neg=.1):
    """
    Generate a random number.

    Parameters
    ----------
    magn_lb : int, default=0
        Lower bound for the magnitude of the number.

    mag_ub : int, default=10
        Upper bound for the magnitude of the number.

    max_decimals : int, default=5
        Maximum number of decimals to which the number can be rounded.

    p_int : float, default=.5
        Probability that the number is an integer.

    p_neg : float, default=.1
        Probability that the number is negative.

    Returns
    -------
    n : float or int
        Randomly generated number.
    """
    n = random() * 10**randint(mag_lb, mag_ub)
    n = -n if random() < p_neg else n
    n = int(n) if random() < p_int else n
    return round(n, randint(0, max_decimals))