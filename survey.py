from flask import render_template
from hemlock import Branch, Page, Label, Hidden, Input, Textarea, Compile as C, route
from hemlock.tools import Assigner, consent_page, completion_page
from hemlock_demographics import basic_demographics

arms = dict(
    no_bonus=("Your score will not affect your payment.", "0"),
    one_for_five=("You will be paid an extra 1 cent for every 5 points.", "score/5"),
    two_for_five=("You will be paid an extra 2 cents for every 5 ponts.", "2*score/5")
)

from bandit import SuccessiveRejectionsAssigner

assigner = SuccessiveRejectionsAssigner(
    {"Arm": arms.keys()},
    target="Score", total_participants=20
)

@route('/survey')
def start():
    instructions, compute_payment = arms[assigner.next()["Arm"]]
    return Branch(
        consent_page("Here is a simple consent form"),
        basic_demographics(page=True),
        Page(
            Label(
                """
                Here is the task description that will be shown in all arms.

                Try out the task at the bottom of the page. You'll be playing for real on the next page.
                """
            ),
            Label(instructions),
            make_keypress_question(compute_payment=compute_payment),
        ),
        Page(
            Label(instructions),
            score_recorder:=Hidden(var="Score", default=0, data_rows=-1),
            bonus_recorder:=Hidden(var="Bonus", default=0, data_rows=-1),
            make_keypress_question(compute_payment, score_recorder, bonus_recorder)
        ),
        Page(
            Label(compile=C.display_score(score_recorder, bonus_recorder)),
            Textarea(
                "Please let us know if you have additional comments about the survey.",
                var="Comments", data_rows=-1
            )
        ),
        completion_page()
    )
    
def make_keypress_question(compute_payment, score_recorder=None, bonus_recorder=None):
    input = Input(
        """
        Press **<span id="nextkey">a</span>**

        Score: **<span id="score">0</span>**

        Bonus: **<span id="bonus">0</span> cents**
        """
    )
    input.js.append(render_template(
        'keypress.js', 
        input=input, 
        compute_payment=compute_payment,
        score_recorder=score_recorder,
        bonus_recorder=bonus_recorder
    ))
    return input

@C.register
def display_score(label, score_recorder, bonus_recorder):
    label.label = f"""
        Your final score was **{score_recorder.response}**.

        You earned a **${float(bonus_recorder.response)/100:.2f}** bonus.
    """
