from sqlalchemy_mutable import partial

from random import choice, randint

numbers = [
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten',
]

def _make_failure_page():
    """Create a page for those who fail attention check

    Returns
    -------
    Page
        Failure page.
    """
    from ..models import Page
    from ..qpolymorphs import Label

    return Page(
        Label(
            '''
            You have been disqualified from the study for failing an attention check.

            Please contact the survey administrator if you believe this is an error.
            '''
        ),
        terminal=True
    )

def attention_check(make_failure_page=_make_failure_page, **kwargs):
    """
    Parameters
    ----------
    make_failure_page : callable, default=make_failure_page
        Returns a terminal page to take participants to after failing the check.

    \*\*kwargs :
        Attributes of the attention check input. Should not include `debug` or `submit`.

    Returns
    -------
    check : Input
        Attention check input.

    Examples
    --------
    ```python
    from hemlock import Page, push_app_context
    from hemlock.tools import attention_check

    app = push_app_context()

    Page(attention_check()).preview()
    ```
    """
    from ..models import Debug as D, Page
    from ..qpolymorphs import Input

    x, y = randint(0, len(numbers)-1), randint(0, len(numbers)-1)
    if x + y < len(numbers):
        plus_minus = choice(['plus', 'minus'])
    else:
        plus_minus = 'minus'
    if plus_minus == 'minus' and y > x:
        x, y = y, x
    answer = x-y if plus_minus == 'minus' else x+y
    return Input(
            '''
            Please spell your answer to the question:

            **What is {} {} {}?**
            '''.format(numbers[x], plus_minus, numbers[y]),
            debug=D.send_keys(numbers[answer]),
            submit=partial(_check_correct_answer, answer, make_failure_page),
            **kwargs
        )

def _check_correct_answer(q, correct_answer, make_failure_page):
    """Checks if the participant responded correctly

    Parameters
    ----------
    q : Question
        Comprehension check question
    correct_answer : int
        Correct answer to the question
    make_failure_page : callable
        Creates a failure page. If `None`, participants who fail the check are
        allowed to continue the survey
    """
    answer = q.response.lower()
    correct = answer in numbers and numbers.index(answer) == correct_answer
    q.data = int(correct)
    if not correct and make_failure_page is not None:
        q.page.branch.pages.insert(q.page.index+1, make_failure_page())