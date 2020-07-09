"""# Submit functions"""

from ..models import Submit
from .utils import convert, correct_choices as correct_choices_

import re

@Submit.register
def correct_choices(question, correct):
    """
    Convert the question's data to a 0-1 indicator that the participant 
    selected the correct choice(s).

    Parameters
    ----------
    question : hemlock.ChoiceQuestion

    correct : list of hemlock.Choice
        Correct choices.

    Notes
    -----
    If the participant can only select one choice, indicate whether the 
    participant selected one of the correct choices.

    Examples
    --------
    ```python
    from hemlock import Check, Submit, push_app_context

    push_app_context()

    check = Check(
    \    '<p>Select one</p>', 
    \    ['correct', 'incorrect', 'also incorrect']
    )
    correct_choice = check.choices[0]
    Submit.correct_choices(check, [correct_choice])
    check.response = correct_choice
    check._submit()
    check.data
    ```

    Out:

    ```
    1
    ```
    """
    question.data = int(correct_choices_(question, correct))

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
    from hemlock import Input, Submit, push_app_context

    push_app_context()

    inpt = Submit.data_type(Input(data='1'), int)
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
    from hemlock import Input, Submit, push_app_context

    push_app_context()

    inpt = Submit.match(Input(data='hello world'), 'hello world')
    inpt._submit()
    inpt.data
    ```

    Out:

    ```
    1
    ```
    """
    try:
        question.data = int(re.match(
            pattern, (question.data or '')) is not None
        )
    except:
        question.data = 0