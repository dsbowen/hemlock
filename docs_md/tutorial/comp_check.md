# Comprehension check

In the previous part of the tutorial, you reviewed page logic.

By the end of this part of the tutorial, you'll be able to set up comprehension checks.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.7/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.7/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Why comprehension checks?

We often give our participants instructions. To make sure they understand the instructions, we give them comprehension checks.

Hemlock has a built-in tool for easy comprehension checks. The structure of a comprehension check is:

1. One or more pages of instructions.
2. One or more pages of 'checks'.
3. If the participant fails a check, they return to the first instructions page.
4. Participants do not have to repeat checks that they pass.
5. We set a limit on the number of attempts participants have to pass each check.

For example, suppose there are two checks, A and B. The participant passes check A but fails check B. He is brought back to the first page of the instructions. After rereading the instructions, he is brought directly to check B, skipping check A.

(Think about what it would take to do this in Qualtrics, or program this from scratch).

## Basic syntax

Although we usually start with jupyter, the logic of comprehension checks is best illustrated by running an app. Open `app.py` and replace `import survey` with `import tmp_survey`. Now make a new file, `tmp_survey.py`, and enter the following:

```python
from hemlock import Branch, Check, Compile as C, Page, Label, Submit as S, route
from hemlock.tools import comprehension_check

@route('/survey')
def start():
    return Branch(
        *comprehension_check(
            instructions=Page(
                Label('<p>Here are some instructions.</p>')
            ),
            checks=Page(
                Check(
                    '<p>Select the correct choice.</p>',
                    ['Correct', 'Incorrect', 'Also incorrect'],
                    compile=[C.clear_response(), C.shuffle()],
                    submit=S.correct_choices('Correct')
                )
            ),
            attempts=3
        ),
        Page(
            Label('<p>You passed the comprehension check!</p>'),
            terminal=True
        )
    )
```

Run the app and play with the comprehension check. Notice that when you don't click the correct choice, the survey brings you back to the instructions page.

### Code explanation

First, we import our standard hemlock objects and the `comprehension_check` tool.

As usual, we return a branch from our navigate function. We begin the branch with a comprehension check. The comprehension check takes a list of instructions pages (or a single instructions page), a list of check pages (or a single check page), and the number of allotted attempts. The `comprehension_check` tool returns a list of instructions + check pages. 

The branch constructor expects pages, not a list of pages, to be passed in as arguments. The asterisk in `*comprehension_check(...)` means *'unlist' the list of instructions + check pages as you pass them into the branch constructor*.

The check page contains a `Check` question. Note that 'check' has different meanings here. A 'check page' in a comprehension check means *a page where you test the participant's understanding of the instructions*. A 'check question' means *a question where you can check one or more choices*.

By default, the check question will record the participant's response and display the choices in their original order. These are both problems for testing comprehension. We don't want participants to simply click choices in order until the hit the right one. To fix this, we add two compile functions; one to clear the response, and one to shuffle the choices.

A participant passes a check page when all of its questions' data evaluate to `True`. So, we'll add a submit function to the check question which converts its data to 1 if the participant selected the correct choice and 0 otherwise (`1` and `0` evaluate to `True` and `False` in most programming languages).

Finally, we set `attempts=3` to give the participant 3 attempts to pass the check. If a participant fails the check 3 times, they'll simply continue the survey. We can require participants to pass the check by not passing an `attempts` parameter.

## Ultimatum game comprehension check

We're going to use a comprehension check to explain the ultimatum game to our participants and test their understanding of it. First, open `app.py` and change `import tmp_survey` back to `import survey`.

### Instructions

Open your notebook and let's preview the instructions page:

```python
from hemlock import Page, Label

# the number of rounds participants play
N_ROUNDS = 5
# the amount of money split
POT = 20

Page(
    Label(
        '''
        <p>You are about to play an ultimatum game. The game involves two
        players: a <b>proposer</b> and a <b>responder</b>. The proposer has 
        ${} to split between him/herself and the responder. The responder 
        names an amount of money such that he/she accepts any proposed 
        split which gives him/her at least this amount, and rejects any 
        proposed split which gives him/her less than this amount.</p>

        <p><b>If the split is accepted, the proposer and responder split the 
        money according to the proposal. If the split is rejected, both 
        players receive $0.</b></p>

        <p>You will play {} rounds of this game. Each round, you will be 
        paired with another randomly selected participant. <b>You will rarely, 
        if ever, play two rounds with the same player.</b>

        <p>We will test your understanding of these instructions on the 
        next page.</p>
        '''.format(POT, N_ROUNDS)
    )
).preview()
```

### Checks

For the check pages, we're going to give participants a hypothetical proposal and response and ask them how much money the proposer and responder receive. We'll do this twice; once where the proposal is accepted, the other where it is rejected.

Additionally, we want to avoid biasing participants' responses by giving them all the same hypothetical proposal-response pairs. So, we'll write a function to randomly generate proposals.

Enter the following in your notebook:

```python
from hemlock import Compile as C, Input

def gen_check_page(accept):
    return Page(
        Label(),
        Input(
            '<p>How much money does the proposer receive?</p>',
            prepend='$',
            append='.00'
        ),
        Input(
            '<p>How much money does the responder receive?</p>',
            prepend='$',
            append='.00'
        ),
        compile=[C.clear_response(), C.random_proposal(accept)]
    )

@C.register
def random_proposal(check_page, accept):
    # WE'LL WRITE THIS FUNCTION IN A MOMENT
    pass

gen_check_page(accept=True).preview()
```

The `gen_check_page` function generates a check page. The `Label` with which the page starts is going to be populated by a randomly generated proposal-response pair which we'll create with the compile function `random_proposal`. Both `gen_check_page` and `random_proposal` take an `accept` argument which indicates whether the proposal will be accepted or rejected.

Now, fill in the `random_proposal` function in the same notebook cell:

```python
from hemlock import Compile as C, Input, Submit as S

from random import randint

...

@C.register
def random_proposal(check_page, accept):
    # randomly generate a proposed split and response
    n = randint(1, POT-1)
    proposal = POT-n, n # proposer receives POT-n, responder receives n
    response = randint(0, n) if accept else randint(n+1, POT)
    # compute the payoff
    payoff = proposal if response<=proposal[1] else (0, 0)
    # describe the proposal and response in the label
    check_page.questions[0].label = '''
    <p>Imagine the proposer proposes the following split:</p>
    <ul>
       <li>Proposer: ${}</li>
       <li>Responder: ${}</li>
    </ul>
    <p>The responder says, "I will accept any proposal which gives 
    me at least ${}."</p>
    '''.format(*proposal, response)
    # add submit functions to verify that the response was correct
    check_page.questions[1].submit = S.match(str(payoff[0]))
    check_page.questions[2].submit = S.match(str(payoff[1]))

gen_check_page(accept=True)._compile().preview()
```

`random_proposal` begins by generating a random proposal. We then generate a random response which will accept the proposal if `accept` is `True` and reject the proposal if `accept` is `False`.

The `payoff` is the proposal if the proposal is accepted and `(0,0)` if the proposal is rejected.

We then fill in the check page's label with the proposal and response.

Finally, we add submit functions to the check page's input questions to verify that the participant's responses match the payoffs.

## Adding a comprehension check to our app

Let's put this all together in `survey.py`:

```python
...
from hemlock.tools import comprehension_check, join

from datetime import datetime
from random import randint

# the number of rounds participants play
N_ROUNDS = 5
# the amount of money split
POT = 20

...

@N.register
def ultimatum_game(start_branch):
    return Branch(
        *comprehension_check(
            instructions=Page(
                # CONTENT OF INSTRUCTIONS PAGE HERE
            ),
            checks=[gen_check_page(accept=True), gen_check_page(accept=False)]
        ),
        Page(
            Label('<p>You passed the check!</p>'),
            terminal=True
        )
    )

def gen_check_page(accept):
    # GEN CHECK PAGE FUNCTION HERE

@C.register
def random_proposal(check_page, accept):
    # RANDOM PROPOSAL FUNCTION HERE
```

Run your app and see your comprehension check at work!

## Summary

In this part of the tutorial, you learned how to add comprehension checks to your studies.

In the next part of the tutorial, you'll learn how to assign participants to conditions.