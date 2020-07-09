from hemlock import Branch, Check, Choice, Compile, Page, Input, Label, Submit, route
from hemlock.tools import comprehension_check

@route('/survey')
def start():
    correct = Choice('correct')
    branch = comprehension_check(
        Branch(),
        instructions=Page(Label('<p>Here are some instructions.</p>')),
        checks=Compile.clear_response(Page(
            Compile.shuffle(Submit.correct_choices(
                Check(
                    '<p>Click the correct choice.</p>',
                    [correct, 'incorrect', 'also incorrect']
                ), 
                correct=[correct]
            ))
        )),
        attempts=3
    )
    branch.pages.append(
        Page(Label('<p>The End!</p>'), terminal=True)
    )
    return branch