"""# Submit functions"""

from ..models import Submit
from .utils import convert, correct_choices as correct_choices_

import re

@Submit.register
def correct_choices(question, *values):
    """
    Convert the question's data to a 0-1 indicator that the participant 
    selected the correct choice(s).

    Parameters
    ----------
    question : hemlock.ChoiceQuestion

    \*values :
        Values of the correct choices.

    Notes
    -----
    If the participant can only select one choice, indicate whether the 
    participant selected one of the correct choices.

    Examples
    --------
    ```python
    from hemlock import Check, Submit as S, push_app_context

    app = push_app_context()

    check = Check(
    \    '<p>Select the correct choice.</p>',
    \    ['correct', 'incorrect', 'also incorrect'],
    \    submit=S.correct_choices('correct')
    )
    check.response = check.choices[0]
    check._submit().data
    ```

    Out:

    ```
    1
    ```
    """
    question.data = int(correct_choices_(question, *values))

@Submit.register
def data_type(question, new_type, *args, **kwargs):
    """
    Convert the quesiton's data to a new type. If the question's data cannot
    be converted, it is changed to `None`.
    
    Parameters
    ----------
    question : hemlock.Question

    new_type : class
    
    \*args, \*\*kwargs :
        Arguments and keyword arguments to pass to the `new_type` constructor.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    inpt = Input(data='1', submit=S.data_type(int))
    inpt._submit()
    inpt.data, isinstance(inpt.data, int)
    ```

    Out:

    ```
    (1, True)
    ```
    """
    question.data, success = convert(question.data, new_type, *args, **kwargs)
    if not success:
        question.data = None

@Submit.register
def match(question, pattern):
    """
    Convert the question's data to a 0-1 indicator that the data matches the
    pattern.

    Parameters
    ----------
    question : hemlock.Question

    pattern : str
        Regex pattern to match.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    inpt = Input(data='hello world', submit=S.match('hello *'))
    inpt._submit().data
    ```

    Out:

    ```
    1
    ```
    """
    try:
        question.data = int(re.fullmatch(
            pattern, (question.data or '')) is not None
        )
    except:
        question.data = 0