"""Utilities"""

from selenium_tools import get_datetime, send_datetime

import math
from datetime import MAXYEAR, MINYEAR, datetime, timedelta
from random import choice, randint, random, randrange, shuffle
from string import ascii_letters, digits

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

def correct_choices(q, *values):
    """
    Parameters
    ----------
    q : hemlock.ChoiceQuestion

    \*values : 
        Values of the correct choices.

    Returns
    -------
    correct : bool
        Indicates that the participant selected the correct choice(s).

    Notes
    -----
    If the participant can only select one choice, indicate whether the 
    participant selected one of the correct choices. If the participant
    selected no choices, indicate whether there were any correct values
    available to select.
    """
    if not q.response:
        return not bool(values)
    data = (
        [c.value for c in q.response] if isinstance(q.response, list) 
        else q.response
    )
    return set(data) == set(values) if q.multiple else data in values

def random_datetime(inpt, min=datetime(1900, 1, 1), max=datetime(2100, 1, 1)):
    def get_dt(attr):
        val = inpt.get_attribute(attr)
        if val:
            return get_datetime(type_, val)

    type_ = inpt.get_attribute('type')
    start = get_dt('min') or min
    stop = get_dt('max') or max
    delta = int((stop - start).days * 24* 60 * 60) # resolution in seconds
    send_datetime(inpt, start + timedelta(seconds=randint(0, delta)))

def random_num(inpt, min=-1000, max=1000, step=.001, p_int=.5):
    start = inpt.get_attribute('min')
    start = min if start == '' else float(start)
    stop = inpt.get_attribute('max')
    stop = max if stop == '' else float(stop)
    step_ = inpt.get_attribute('step')
    step_ = step if step_ in ('', 'any') else float(step_)
    x = start + random() * (stop - start)
    x = round(x / step) * step_
    inpt.send_keys(str(int(x) if random() < p_int else x))

def random_str(inpt, maxlength=100, p_whitespace=.2):
    chars = ascii_letters + digits
    chars = list(chars) + [' '] * int(p_whitespace*len(chars))
    # response length follows exponential distribution
    magnitude = math.log(inpt.get_attribute('maxlength') or maxlength)
    length = int(random() * 10**randint(1,magnitude))
    inpt.send_keys(''.join([choice(chars) for i in range(length)]))