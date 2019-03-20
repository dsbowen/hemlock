###############################################################################
# Comprehension check
# by Dillon Bowen
# last modified 03/20/2019
###############################################################################

# Notes:
# To pass a comprehension check, either the check's post function must
# evaluate to True, or (if no post function) the data of all questions 
# must evaluate to True
# Lists of instruction page and check page ids must be non-empty

from hemlock.tools.global_vars import modg, g
from hemlock.tools.query import query
from hemlock.models.branch import Branch
from hemlock.models.page import Page



# Return a specialized branch for comprehension checks
# arguments:
    # instruction ids: list of ids of instruction pages
    # check_ids: list of ids for comprehension check pages
    # next and next_args: next function and arguments
    # max_attemtps: maximum number of attempts per comprehension check page
# set attempts to 1 (first attempt)
# create comprehension check branch
# add instructions and checks to branch
# failed comprehension checks go back to first instructions page
# set post function on comprehension checks to verify answers
def comprehension_check(
        instruction_ids, check_ids,
        next=None, next_args=None, max_attempts=None):
        
    if not (instruction_ids and check_ids):
        raise ValueError(
                'Comprehension check must have instruction and check pages')
        
    modg({'_attempt': 1, '_max_attempts': max_attempts})
    b = Branch(next=next, next_args=next_args)
    
    instructions, checks = query([instruction_ids, check_ids], Page)
    [i.branch(b) for i in instructions]
    [c.branch(b) for c in checks]
    [c.back_to(instructions[0]) for c in checks]
    [set_post_function(c, instruction_ids[-1]) for c in checks]
    
    return b
    
# Set the post function for a comprehension check page
# last_instructions_id is the id of the last instructions page
def set_post_function(check, last_instructions_id):
    args = {'last_instructions_id': last_instructions_id,
            'post': check._post_function, 'post_args': check._post_args}
    check.post(verify_answers, args)
    
# Verify that the answers on the comprehension check page are correct
# return if responses are invalid
# return if responses passed the check or attempt limit was reached
# otherwise, increment attempt and go back to first instruction page
# first instruction page contains an error message
# last instructions page brings participant back to current check
def verify_answers(check, last_instructions_id, post, post_args):
    if not all([q._validate() for q in check._questions.all()]):
        return
        
    if passed(check, post, post_args) or attempt_limit_reached():
        modg({'_attempt':1})
        return
        
    modg({'_attempt':g('_attempt')+1})
    [q.reset_default() for q in check._questions]
    check.direction_from('back')
    
    first_instructions = check.get_back_to()
    first_instructions._questions[0].error(
        'Your response was incorrect. Please reread the instructions.')
    
    last_instructions = query(last_instructions_id, Page)
    last_instructions.forward_to(check)
    
# Indicates participant passed the comprehension check
# either check post function returns bool
# or data for all questions must be True
def passed(check, post, post_args):
    if post is not None:
        return check._call_function(post, post_args)
    return all([q.get_data() for q in check._questions.all()])
    
# Indicates participant has reached their attempt limit
def attempt_limit_reached():
    return g('_attempt') == g('_max_attempts')