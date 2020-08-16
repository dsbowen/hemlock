# Random assignment

In the previous part of the tutorial, you leanred how to add comprehension checks to your studies.

By the end of this part of the tutorial, you'll be able to randomly assign your participants to conditions, for example treatment and control.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.8/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.8/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Participant
from hemlock.tools import Assigner

part = Participant.gen_test_participant()
conditions = {'Treatment': (0,1), 'Level': ('low','med','high')}
assigner = Assigner(conditions)
assigner.next()
```

Out:

```
{'Treatment': 0, 'Level': 'low'}
```

The `Assigner` randomly and evenly assigns participants to conditions, and easily handles factorial designs. It automatically records the assignment in the participant's embedded data:

```python
[(e.var, e.data) for e in part.embedded]
```

Out:

```
[('Treatment', 0), ('Level', 'low')]
```

## Random assignment in our app

In `survey.py`:

```python
...
from hemlock.tools import Assigner, comprehension_check, join

from datetime import datetime
from random import randint

# the number of rounds participants play
N_ROUNDS = 5
# the amount of money split
POT = 20

assigner = Assigner({'Proposer': (0, 1)})

...

@N.register
def ultimatum_game(start_branch=None):
    proposer = assigner.next()['Proposer']
    return Branch(
        *comprehension_check(
            # COMPREHENSION CHECK ARGUMENTS HERE
        ),
        Page(
            Label(
                '''
                <p>You are about to play an ultimatum game as a <b>{}</b>.</p>
                '''.format('proposer' if proposer else 'responder')
            ),
            terminal=True
        )
    )
```

Run your app and pass the comprehenion check to see which condition you've been assigned to.

## Summary

In this part of the tutorial, you learned how to assign participants to conditions.

In the next part of the tutorial, you'll implement the proposer branch of the ultimatum game.