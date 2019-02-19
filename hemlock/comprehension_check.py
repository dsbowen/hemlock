###############################################################################
# Comprehension check
# by Dillon Bowen
# last modified 02/19/2019
###############################################################################

'''
TODO
Make this more flexible:
    multiple instruction pages
    multiple comprehension check pages
    record how many attempts they took to get correct
    may need a separate class
'''

'''
Inputs:
    instructions_id: ID of instructions page
    check_id: ID of comprehension check page
    next function and args
    maximum number of attempts allowed
Requirements:
    data for comprehension check questions must be True/False
    comprehension check page must not have post function
'''

from hemlock.query import query
from hemlock.g import modg, g
from hemlock.models.branch import Branch
from hemlock.models.page import Page

# Return a specialized branch for comprehension checks
def comprehension_check(instructions_id, check_id,
    next=None, next_args=None, max_attempts=None):
    
    modg({'_attempt':1,'_max_attempts':max_attempts})
    
    b = Branch(next=next, next_args=next_args)
    instructions, check = query([instructions_id, check_id], Page)
    [p.branch(b) for p in [instructions, check]]
    check.post(condition_is_met, instructions_id)
    
    return b
    
# Check if the condition for determining correct responses was met
# if not, check goes back to instructions
# instructions page includes an error message
def condition_is_met(check, instructions_id):
    if not all([q._validate() for q in check._questions.all()]):
        return
    passed = all([q.get_data() for q in check._questions.all()])
    limit_reached = g('_attempt') == g('_max_attempts')
    if passed or limit_reached:
        return
    modg({'_attempt':g('_attempt')+1})
    check._direction_from = 'back'
    instructions = query(instructions_id,Page)
    instructions._questions[0].error(
        'Your response was incorrect. Please reread the instructions.')