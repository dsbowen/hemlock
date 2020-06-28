"""Utilities"""

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

def correct_choices(q, *correct):
    """
    Parameters
    ----------
    q : hemlock.ChoiceQuestion

    \*correct : hemlock.Choice
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
    return q.response == correct if q.multiple else q.response in correct