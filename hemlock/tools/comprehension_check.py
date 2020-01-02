"""Comprehension check

A comprehension check consists of 'instruction' pages followed by 'check' 
pages. 

The data in all questions of a check page must evaluate to `True` to pass 
the check.

When you fail a check, you are brought back to the first instructions page. 
However, once you reread the instructions, you do not have to repeat any 
checks you already passed.
"""

ERROR_MSG = """
<p>Your response was incorrect.</p>
<p>Please reread the instructions before continuing.</p>
"""

def comprehension_check(instructions=[], checks=[], attempts=None):
    """Return a comprehension check branch"""
    assert instructions and checks, '`instructions` and `checks` must be non-empty lists of Pages'
    from hemlock.app import db
    from hemlock.database import Branch, Submit
    b = Branch(pages=(instructions+checks))
    for check in checks:
        check.back_to = instructions[0]
        Submit(check, verify_data, kwargs={
            'last_instr_page': instructions[-1],
            'curr_attempt': 1,
            'attempts': attempts
        })
        db.session.commit()
    return b

def verify_data(check, last_instr_page, curr_attempt, attempts):
    if all(q.data for q in check.questions) or curr_attempt == attempts:
        if check != check.branch.pages[-1]: # last check page
            last_instr_page.forward_to = check.branch.pages[check.index+1]
        return
    check.back_to.error = ERROR_MSG
    check.direction_from = 'back'
    check.submit_functions[-1].kwargs['curr_attempt'] = curr_attempt + 1