# Responder branch

In the previous part of the tutorial, you implemented the proposer branch.

In this part of the tutorial, you'll implement the responder branch.

The responder branch is similar to the proposer branch. For a great exercise, see if you can create it yourself without looking at my code.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.10/survey.py" target="_blank">`survey.py`</a> file should look like at the end of this part of the tutorial.

## Adding the responder branch to our survey

Because the responder branch is similar to the proposer branch, we'll skip the notebook and work straight in `survey.py`. I'll point out the differences as we go along.

First, let's add a navigate function to the end of our ultimatum game branch to bring us to the responder branch:

```python
...

@N.register
def ultimatum_game(start_branch=None):
    proposer = assigner.next()['Proposer']
    return Branch(
        # PAGES HERE
        navigate=N.proposer_branch() if proposer else N.responder_branch()
    )

...

@N.register
def responder_branch(ultimatum_game_branch=None):
    branch = Branch()
    for round_ in range(N_ROUNDS):
        response_input = gen_response_input(round_+1)
        branch.pages.append(Page(response_input))
        branch.pages.append(Page(
            Label(compile=C.responder_outcome(response_input)),
            cache_compile=True
        ))
    branch.pages.append(Page(
        Label('<p>Thank you for completing the hemlock tutorial!</p>'),
        terminal=True        
    ))
    return branch
```

Like in the proposer branch, we add two pages to the responder branch for each of `N_ROUNDS`. Just as the first of these two pages asked the proposer for the proposal in the proposer branch, the first of these two pages asks the responder for their response in the responder branch. Like in the proposer branch, the second of these pages displays the outcome of the round.

## The responder input

Just as the proposer's input was created with `gen_proposal_input`, the responder's input is created with `gen_response_input`:

```python
...

def gen_response_input(round_):
    return Input(
        '''
        <p><b>Round {} of {}</b></p>
        <p>The proposer has ${} to split between him/herself and you. Complete
        this sentence:</p>
        <p>I will accept any proposal which gives me at least</p>
        '''.format(round_, N_ROUNDS, POT),
        prepend='$', append='.00', var='Response',
        validate=V.range_val(0, POT),
        submit=S.data_type(int)
    )
```

As before, we add valiation so that the input must be between 0 and the size of the pot, and a submit function which converts the data to an integer.

## Displaying the responder outcome

We register a compile function to display the responder outcome.

```python
...

@C.register
def responder_outcome(outcome_label, responder_input):
    # get the response
    response = responder_input.data
    # randomly select a proposal
    proposal_inputs = Input.query.filter(
        Input.var=='Proposal', Input.data!=None
    ).all()
    if proposal_inputs:
        # randomly choose a proposal
        n = random.choice(proposal_inputs).data
    else:
        # no proposals are available
        # e.g. if this is the first participant
        n = randint(0, POT)
    proposal = POT-n, n
    # compute the payoff
    accept = response <= proposal[1]
    payoff = proposal if accept else (0, 0)
    # record results as embedded data
    outcome_label.page.embedded = [
        Embedded('Proposal', proposal[1]),
        Embedded('Accept', int(accept)),
        Embedded('ProposerPayoff', payoff[0]),
        Embedded('ResponderPayoff', payoff[1])
    ]
    # describe the outcome of the round
    outcome_label.label = '''
        <p>The proposer proposed the following split:</p>
        <ul>
            <li>Proposer: ${}</li>
            <li>You: ${}</li>
        </ul>
        <p>You said you will accept any proposal which gives you at 
        least ${}.</p>
        <p><b>You {} the proposal, giving you a payoff of ${}.</b></p>
    '''.format(
        *proposal, response, 'accepted' if accept else 'rejected', payoff[1]
    )
```

This is similar to the `proposer_outcome` compile function. First, it gets the responder's response. Second, it matches the responder with a random proposer. If no proposer is avaiable (e.g. if the responder is the first participant in the survey), it generates a random proposal. Third, we compute the payoff for the round and record it using embedded data. Finally, we update the label to display the outcome of the round to the proposer.

Run the app to see what the survey looks like in the responder condition.

## Summary

In this part of the tutorial, you implemented the responder branch.

In the next part of the tutorial, you'll learn how to use hemlock's cutom debugger to make sure everything is running smoothly.