"""# Comprehension check"""

ERROR_MSG = """
Your response was incorrect.<br/>
Please reread the instructions before continuing.
"""

def comprehension_check(instructions, checks, attempts=None):
    """
    A comprehension check consists of 'instruction' pages followed by 'check' 
    pages. The data of all questions in a check page must evaluate to `True` 
    to pass the check. When a participant fails a check, he is brought back to 
    the first instructions page. 
    
    Participants only have to pass each check once. For example, suppose there 
    are two checks, A and B. The participant passes check A but fails check B. 
    He is brought back to the first page of the instructions. After rereading 
    the instructions, he is brought directly to check B, skipping check A.

    Parameters
    ----------
    instructions : hemlock.Page or list of hemlock.Page
        Instruction page(s).

    checks : hemlock.Page or list of hemlock.Page
        Check page(s).

    attempts : int or None, default=None
        Number of attempts allotted. Participants are allowed to proceed with 
        the survey after exceeding the maximum number of attempts. If `None`, 
        participants must pass the comprehension check before continuing the 
        survey.

    Returns
    -------
    pages : list of hemlock.Page
        List of instructions pages + check pages.

    Notes
    -----
    This function adds a `hemlock.Submit` function to each check page. This 
    must be the last submit function of each check page. 

    Examples
    --------
    We have two files in our root directory. In `survey.py`:

    ```python
    from hemlock import Branch, Page, Label, Input, Submit as S, route
    from hemlock.tools import comprehension_check

    @route('/survey')
    def start():
    \    return Branch(
    \        *comprehension_check(
    \            instructions=Page(
    \                Label('<p>Here are some instructions.</p>')
    \            ),
    \            checks=Page(
    \                Input(
    \                    '<p>Enter "hello world" or you... shall not... PASS!</p>',
    \                    submit=S.match('hello world')
    \                )
    \            )
    \        ),
    \        Page(
    \            Label('<p>You passed the comprehension check!</p>'),
    \            terminal=True
    \        )
    \    )
    ```

    In `app.py`:

    ```python
    import survey

    from hemlock import create_app

    app = create_app()

    if __name__ == '__main__':
    \    from hemlock.app import socketio
    \    socketio.run(app, debug=True)
    ```

    Run the app with:

    ```
    $ python app.py # or python3 app.py
    ```

    Open your browser to <http://localhost:5000/>.
    """
    assert instructions and checks, (
        '`instructions` and `checks` must be non-empty lists of hemlock.Pages'
    )
    from ..models import Submit
    if not isinstance(instructions, list):
        instructions = [instructions]
    if not isinstance(checks, list):
        checks = [checks]
    for check in checks:
        check.back_to = instructions[0]
        check.submit.append(Submit(
            _verify_data, 
            instructions[-1], 
            curr_attempt=1, 
            attempts=attempts
        ))
    return instructions + checks

def _verify_data(check, last_instr_page, curr_attempt, attempts):
    """
    Verify that the data on the comprehension page is correct.

    Parameters
    ----------
    check : hemlock.Page
        Check page.

    last_instr_page : hemlock.Page
        Last instructions page.

    curr_attempt : int
        Current attempt number.

    attempts : int or None
        Maximum number of attempts.
    """
    if (
        all(q.data for q in check.questions) 
        or (attempts is not None and curr_attempt >= attempts)
    ):
        if check != check.branch.pages[-1]:
            # this check does not have to be repeated
            last_instr_page.forward_to = check.branch.pages[check.index+1]
            pass
        return
    check.back_to.error = ERROR_MSG
    check.direction_from = 'back'
    check.submit[-1].kwargs['curr_attempt'] = curr_attempt + 1