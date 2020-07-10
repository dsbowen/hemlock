# Proposer branch

In the previous part of the tutorial, you learned how to randomly assign participants to conditions.

In this part of the tutorial, you'll implement the proposer branch of the ultimatum game.

## The proposal input

First, we'll write a function to generate an input question where the proposer will input the proposed split. Enter the following in your jupyter notebook:

```python
from hemlock import Input, Label, Page, Submit, Validate

N_ROUNDS = 5
POT = 20

def gen_proposal_input(round_):
    return Submit.data_type(
        Validate.range_val(
            Input(
                '''
                <p><b>Round {} of {}</b></p>
                <p>You have ${} to split between you and the responder. How 
                much money would you like to offer to the responder?</p>
                '''.format(round_, N_ROUNDS, POT),
                prepend='$',
                append='.00',
                var='Proposal'
            ),
            min_=0, max_=POT
        ),
        int
    )

path = Page(gen_proposal_input(1)).preview()
```

This function generates an input which asks the proposer how much money they would like to offer to the responder. We record the data in a variable named `'Proposal'`.

We add range validation so that the proposer inputs an integer between 0 and the size of the pot. We also add a submit function which converts the data type to an integer.

**Note.** For input questions, the data are recorded as strings. We want to reference this question's data as an integer, so we use `Submit.data_type(Input(), int)` to convert it when the page is submitted.

## Finding a responder

We can use the [SQLAlchemy Query API](https://docs.sqlalchemy.org/en/13/orm/query.html) to pair the proposer with a random responder this round. 

In our notebook, we'll create an input question with the variable name `'Response'`. We'll then use the Query API to get all input questions with that variable name and select the data from one of them at random:

```python
import random

response_input = Input(var='Response', data=5)
response_inputs = Input.query.filter(
    Input.var=='Response', Input.data!=None
).all()
random.choice(response_inputs).data
```

Out:

```
5
```

As expected, this matches the data from our response input.

## Displaying the proposer outcome

Now we want to display the outcome of the round to the proposer. This calls for a compile function:

```python
from hemlock import Compile, Embedded

from random import randint

@Compile.register
def proposer_outcome(outcome_label, proposal_input):
    # get the proposal
    proposal = POT-proposal_input.data, proposal_input.data
    # get all responses
    response_inputs = Input.query.filter(
        Input.var=='Response', Input.data!=None
    ).all()
    if response_inputs:
        # randomly choose a response
        response = random.choice(response_inputs).data
    else:
        # no responses are available
        # e.g. if this is the first participant
        response = randint(0, POT)
    # compute the payoff
    accept = response <= proposal[1]
    payoff = proposal if accept else (0, 0)
    # record results as embedded data
    outcome_label.page.embedded = [
        Embedded('Response', response),
        Embedded('Accept', int(accept)),
        Embedded('ProposerPayoff', payoff[0]),
        Embedded('ResponderPayoff', payoff[1])
    ]
    # describe the outcome of the round
    outcome_label.label = '''
        <p>You proposed the following split:</p>
        <ul>
            <li>You: ${}</li>
            <li>Responder: ${}</li>
        </ul>
        <p>The responder said they will accept any proposal which gives
        them at least ${}.</p>
        <p><b>Your proposal was {}, giving you a payoff of ${}.</b></p>
    '''.format(
        *proposal, response, 'accepted' if accept else 'rejected', payoff[0]
    )

proposal_outcome_page = Page(Compile.proposer_outcome(
    Label(), Input(data=10)
))
path = proposal_outcome_page._compile().preview()
```

Let's go through this step by step.

First, we get the proposal from the proposal input question. Remember that we converted the data for this input to an integer using a submit function. The data for this input is the amount of money the proposer offered to the responder, meaning that the proposed split is `(POT-proposal_input.data, proposal_input.data)`.

Second, we use the Query API to randomly select a response input question. We modify our above code to account for the fact that, if the first participant is a proposer, there won't be any responses to choose from. So, if our query can't find any response input questions, we return a random response.

Third, we compute the payoff and record the results of the round using embedded data.

Finally, we set the outcome label's `label` attribute to display the outcome of the round.

Notice that the outcome of the round is recorded in the proposer's outcome page's embedded data:

```python
[(e.var, e.data) for e in proposal_outcome_page.embedded]
```

Out:

```
[('Response', 5),
 ('Accept', 1),
 ('ProposerPayoff', 10),
 ('ResponderPayoff', 10)]
```

## Adding the proposer branch to our survey

### Navigating to the proposer branch

We'll begin by modifying the ultimatum game branch to navigate to the proposer branch if the participant was assigned to be a proposer. In `survey.py`:

```python
...

@Navigate.register
def ultimatum_game(start_branch):
    ...
    proposer = assigner.next()['Proposer']
    branch.pages.append(Page(
        Label('''
            <p>You are about to play an ultimatum game as a <b>{}</b>.</p>
        '''.format('proposer' if proposer else 'responder')
        ),
        # REMOVE terminal=True
    ))
    if proposer:
        return Navigate.proposer_branch(branch)
    else:
        # WE'LL IMPLEMENT THE RESPONDER BRANCH IN THE NEXT PART OF THE TUTORIAL
        return branch

...
```

### The proposer branch navigate function

Next we'll add our proposer navigate function to the bottom of `survey.py`:

```python
from hemlock import Branch, Check, Compile, Embedded, Input, Label, Navigate, Page, Range, Select, Submit, Validate, route
from hemlock.tools import Assigner, comprehension_check, join

import random # ADD THIS IMPORT AT THE TOP OF THE FILE
from datetime import datetime
from random import randint

...

@Navigate.register
def proposer_branch(ultimatum_game_branch=None):
    branch = Branch()
    for round_ in range(N_ROUNDS):
        proposal_input = gen_proposal_input(round_+1)
        branch.pages.append(Page(proposal_input))
        branch.pages.append(Page(Compile.proposer_outcome(
            Label(), proposal_input
        )))
    branch.pages.append(Page(
        Label('<p>Thank you for completing the hemlock tutorial!</p>'),
        terminal=True      
    ))
    return branch
```

This navigate function simply adds two pages to the proposer branch for each of `N_ROUNDS`. The first page asks the proposer to propose a split. The second page displays the outcome of the round.

### Generating the proposal input and outcome label

Finally, we'll add the `gen_proposal_input` and `proposer_outcome` functions we wrote in our notebook:

```python
...

def gen_proposal_input(round_):
    # AS IN THE NOTEBOOK

@Compile.register
def proposer_outcome(outcome_label, proposal_input):
    # AS IN THE NOTEBOOK
```

Run the app and see what the survey looks like in the proposer condition.

## Summary

In this part of the tutorial, you implemented the proposer branch.

In the next part of the tutorial, you'll implement the responder branch.