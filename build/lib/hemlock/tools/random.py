"""# Randomization tools"""

from ..models import Embedded

from flask_login import current_user

from itertools import combinations, cycle, permutations, product
from operator import itemgetter
from random import choice, shuffle
from string import ascii_letters, digits

def key(len_=90):
    """
    Parameters
    ----------
    len_ : int, default=90
        Length of the key to generate.

    Returns
    -------
    key : str
        Randomly generated key of ascii letters and digits of specificed 
        length.

    Examples
    --------
    ```python
    from hemlock import tools

    tools.key(10)
    ```

    Out:

    ```
    gpGmZuRfF7
    ```
    """
    chars = ascii_letters + digits
    return ''.join(choice(chars) for i in range(len_))


class Randomizer():
    """
    Evenly randomizes over a set of elements.

    Parameters
    ----------
    elements : iterable
        Set of elements over which to randomize.

    r : int, default=1
        Size of the subset of elements to select.

    combination : bool, default=True
        Indicates randomization over combinations of the elements, as opposed 
        to permutations.

    Attributes
    ----------
    elements : iterable
        Set from the `elements` parameter.

    Examples
    --------
    ```python
    from hemlock.tools import Randomizer

    elements = ('world','moon','star')
    randomizer = Randomizer(elements, r=2, combination=False)
    randomizer.next()
    ```

    Out:

    ```
    ('moon', 'world')
    ```
    """
    def __init__(self, elements, r=1, combination=True):
        self.elements = elements
        idx = list(range(len(elements)))
        iter_ = combinations(idx, r) if combination else permutations(idx, r)
        iter_ = list(iter_)
        shuffle(iter_)
        self._iter = cycle(iter_)
        
    def next(self):
        """
        Returns
        -------
        subset :
            Selected subset of elements.
        """
        return itemgetter(*next(self._iter))(self.elements)


class Assigner(Randomizer):
    """
    Evenly assigns participants to conditions. Inherits from 
    `hemlock.tools.Randomizer`.

    Parameters
    ----------
    conditions : dict
        Maps condition variable name to iterable of possible assignments.

    Attributes
    ----------
    keys : iterable
        Condition variable names.

    elements : iterable
        All possible combinations of condition values to which a participant may be assigned.

    Examples
    --------
    ```python
    from hemlock import Participant, push_app_context
    from hemlock.tools import Assigner

    push_app_context()

    part = Participant.gen_test_participant()
    conditions = {'Treatment': (0,1), 'Level': ('low','med','high')}
    assigner = Assigner(conditions)
    assigner.next()
    ```

    Out:

    ```
    {'Treatment': 1, 'Level': 'low'}
    ```

    In:

    ```python
    [(e.var, e.data) for e in part.embedded]
    ```

    Out:

    ```
    [('Treatment', 0), ('Level', 'low')]
    ```
    """

    def __init__(self, conditions):
        self.keys = conditions.keys()
        super().__init__(tuple(product(*conditions.values())))
        
    def next(self):
        """
        Assigns the participant to a condition. The condition assigment 
        updates the participant's metadata.

        Returns
        -------
        assignment : dict
            Maps condition variable names to assigned conditions.
        """
        assignment = super().next()
        assignment = {key: val for key, val in zip(self.keys, assignment)}
        try:
            current_user.embedded += [
                Embedded(key, val, -1) for key, val in assignment.items()
            ]
        except:
            print('Unable to update participant metadata.')
        return assignment