"""Randomization tools

This module defines the following randomization tools:
1. `random_key`: generates a key of random ascii letters and digits
2. `even_randomize`: evenly randomize over a set of elements
3. `random_assign`: randomly assign participants to conditions
"""

from hemlock.app import db
from hemlock.database.data import Embedded

from itertools import combinations, permutations, product
from operator import itemgetter
from random import choice, shuffle
from string import ascii_letters, digits

def random_key(length=90):
    chars = ascii_letters + digits
    return ''.join(choice(chars) for i in range(length))

def even_randomize(tag, elements, r=None, combination=False):
    """Evenly randomize over a set of elements
    
    This method returns a randomly chosen or permuted subset (of size `r`) of 
    `elements`.
    """
    randomizer = Randomizer.query.filter_by(tag=tag).first()
    if randomizer is None:
        randomizer = Randomizer(tag, len(elements), r, combination)
    return itemgetter(*randomizer.select())(elements)

def random_assign(parent, tag, conditions):
    """Randomly assign to conditions

    `conditions` is a dict mapping condition variable names to a list/tuple of 
    possible condition values.

    This function stores assignments as embedded data in the parent. It 
    returns a dict mapping condition variable names to the assigned condition.
    """
    condition_vals = list(product(*conditions.values()))
    assignments = zip(conditions.keys(), even_randomize(tag, condition_vals, 1))
    assignments = {key: val for key, val in assignments}
    [
        Embedded(parent, all_rows=True, data=val, var=var) 
        for var, val in assignments.items()
    ]
    return assignments


class Randomizer(db.Model):
    """Randomizer

    `Randomizer`s store a randomly ordered list of `r`-length subsets of 
    combinations or permutations of element indices, (`iter`). The `select`
    method selects the next element in `iter`.

    All randomizer instances are uniquely identified by a `tag`.
    """
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)
    iter = db.Column(db.PickleType)
    head = db.Column(db.Integer, default=0)

    def __init__(self, tag, n_elements, r=None, combination=False):
        db.session.add(self)
        db.session.flush([self])
        self.tag = tag
        if combination:
            iter_ = combinations(list(range(n_elements)), r)
        else:
            iter_ = permutations(list(range(n_elements)), r)
        iter_ = list(iter_)
        shuffle(iter_)
        self.iter = iter_

    def select(self):
        self.head = (self.head + 1) % len(self.iter)
        return self.iter[self.head]