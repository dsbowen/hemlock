###############################################################################
# Randomization tools
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

'''
MAKE RANDOM_ASSIGNMNET MORE ELEGANT
    b = Branch()
    
    disclosed = [0,1]
    smart_anchor = [0,1]
    ALL OF THE FOLLOWING SHOULD BE ONE LINE
    DISCLOSED, SMART_ANCHOR = RANDOM_ASSIGNMNET('CONDITION'[DISLCOSED,SMART_ANCHOR])
    knowledge, anchor = random_assignment('condition',[disclosed,smart_anchor])
    disclosed = Question(branch=b, qtype='embedded', var='disclosed', data=knowledge, all_rows=True)
    smart_anchor = Question(branch=b, qtype='embedded', var='smart_anchor', data=anchor, all_rows=True)
'''

from hemlock import db
from itertools import permutations, combinations, product
from operator import itemgetter
from copy import deepcopy

'''
Randomize evenly over a sorted list of elements
input:
    tag - randomization identifier
    elements - sorted list of elements
    choose_num - number of elements chosen
    combination - randomization over combiantions (as opposed to permutations)
'''
def even_randomize(tag, elements, choose_num=None, combination=False):
    randomizer = Randomizer.query.filter_by(tag=tag).first()
    if choose_num is None:
        choose_num = len(elements)
    if randomizer is None:
        randomizer = Randomizer(tag, len(elements), choose_num, combination)
    selected = randomizer.select()
    return itemgetter(*selected)(elements)
    
'''
Randomly assign participant to condition
input:
    tag - randomization identifier
    conditions - sorted list of conditions
'''
def random_assignment(tag, conditions):
    conditions = list(product(*conditions))
    return even_randomize(tag, conditions, 1)

'''
Data:
tag - unique randomizer identification tag
combination - indicates randomization over combinations (versus permutations)
stored - dictionary mapping keys to number of presentations
'''
class Randomizer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, unique=True)
    combination = db.Column(db.Boolean)
    stored = db.Column(db.PickleType)
    
    # Create empy dictionary mapping randomization keys to number of presentations
    def __init__(self, tag, length, choose_num, combination=False):
        db.session.add(self)
        db.session.commit()
    
        self.tag = tag
        self.combination = combination
        
        if combination:
            keys = combinations(range(length), choose_num)
        else:
            keys = permutations(range(length), choose_num)
        self.stored = {key:0 for key in keys}
        
    # Select a key from keys with minimum number of presentations
    def select(self):
        key = min(self.stored, key=self.stored.get)
        temp = deepcopy(self.stored)
        temp[key] += 1
        self.stored = deepcopy(temp)
        db.session.commit()
        return list(key)
        
    

