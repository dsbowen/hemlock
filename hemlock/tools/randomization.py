###############################################################################
# Randomization tools
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

from hemlock.factory import db
from hemlock.models.question import Question
from itertools import permutations, combinations, product
from operator import itemgetter
from copy import deepcopy



'''
Randomize evenly over a sorted list of elements
arguments:
    tag: randomization identifier
    elements: sorted list of elements
    choose_num: number of elements chosen
    combination: indicates randomization over combiantions 
        (as opposed to permutations)
returns: randomized list of elements
'''
def even_randomize(tag, elements, choose_num=None, combination=False):
    randomizer = Randomizer.query.filter_by(tag=tag).first()
    if randomizer is None:
        randomizer = Randomizer(tag, len(elements), choose_num, combination)
    if choose_num is None:
        choose_num = len(elements)
    return itemgetter(*randomizer.select())(elements)


  
'''
Randomly assign participant to condition
arguments:
    b: branch for the embedded data
    tag: randomization identifier
    vars: list of variables to which conditions are assigned
    condition_vals: sorted list of condition values
returns: list of assigned condition values
'''
def random_assignment(b, tag, vars, condition_vals):
    condition_vals = list(product(*condition_vals))
    assignments = even_randomize(tag, elements=condition_vals, choose_num=1)
    [Question(branch=b, qtype='embedded', var=var, all_rows=True, data=data)
        for (var,data) in zip(vars,assignments)]
    if len(assignments)==1:
        return assignments[0]
    return assignments



'''
Columns:
    tag: unique randomizer identification tag
    combination: indicates randomization over combinations 
        (as opposed to permutations)
    permutations: queue of unique permutations of elements
        (may actually be a queue of combinations if combination=True)
    head: head of permutations queue
'''
class Randomizer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, unique=True)
    combination = db.Column(db.Boolean)
    permutations = db.Column(db.PickleType)
    head = db.Column(db.Integer, default=0)
    
    # Create a list of permutations or combinations of the elements
    # arguments:
        # length: length of elements list over which randomization occurs
        # choose_num: number of elements to be chosen from the elements list
    def __init__(self, tag, length, choose_num, combination=False):
        db.session.add(self)
        db.session.commit()
    
        self.tag = tag
        self.combination = combination
        
        if combination:
            self.permutations = list(combinations(range(length), choose_num))
        else:
            self.permutations = list(permutations(range(length), choose_num))
        shuffle(self.permutations)
        
    # Return the current permutation (combination)
    # increment head
    def select(self):
        permutation = self.permutations[self.head]
        self.head = (self.head + 1) % len(self.permutations)
        return permutation
        
    

