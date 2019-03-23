###############################################################################
# Hemlock survey template
# by Dillon Bowen
# last modified 03/12/2019
###############################################################################

'''
# import hemlock package, configuration class, and texts
from hemlock import *
from config import Config
from texts import *

def Start():
    raise NotImplementedError()
      
# create the application (survey)
app = create_app(
    Config,
    start=Start,
    password='',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv')
    
# hemlock shell
import hemlock_shell
'''

###############################################################################
# Hemlock survey template
# by Dillon Bowen
# last modified 03/12/2019
###############################################################################

# import hemlock package, configuration class, and texts
from hemlock import *
from config import Config
from texts import *
from random import shuffle

# Consent page
def Start():
    b = Branch(next=IndicatePreferences)
    p = Page(b)
    q = Question(p, consent)
    q = Question(p, 'Enter your MTurk ID:', 
                 qtype='free', var='workerId', all_rows=True)
    Validator(q, require)
    return b
    
    
    
###############################################################################
# Indicate preferences
###############################################################################
    
# Indicate preferences
def IndicatePreferences():
    b = Branch()
    
    # add preference labels as embedded data
    [Question(branch=b, qtype='embedded', var='preference_label', data=text)
        for text in preference_estimate_texts]
    
    # randomly assign to disclosed or surprise condition
    disclosed = random_assignment(b, 'condition', ['disclosed'], [[0,1]])
    modg({'disclosed':disclosed})
    
    # preference instructions
    p = Page(b)
    q = Question(p, intro_preferences)
    
    # add multiple choice questions to page to indicate preferences
    p = Page(b)
    [create_preference_question(p.id, i) 
        for i in range(len(preference_question_texts))]
    p.randomize()
    
    # navigate to disclosed comprehension check
    # or surprise condition intro
    if g('disclosed'):
        b.next(DisclosedComprehension)
    else:
        b.next(SurpriseIntro)
    
    return b
        
# Create a preference indication question and add to page
def create_preference_question(page_id, i):
    page = query(page_id, Page)
    q = Question(page, preference_question_texts[i], 
                 qtype='single choice', var='preference')
    Choice(q, preference_options[i][1], value=1, label='yes')
    Choice(q, preference_options[i][0], value=0, label='no')
    Validator(q, require)
    q.randomize()
    
    
    
###############################################################################
# Instructions and comprehension checks
###############################################################################
    
# Disclosed condition comprehension check
# create instructions page
# create comprehension check page
# return comprehension check branch
def DisclosedComprehension():        
    instructions = Page()
    Question(instructions, disclosed_instructions)
    
    check = Page()
    q = Question(
        check, comprehension_text, qtype='single choice', 
        var='Comprehension', compile=rerandomize, all_rows=True)
    Choice(q, disclosed_incorrect1, value=0, label='incorrect1')
    Choice(q, disclosed_incorrect2, value=0, label='incorrect2')
    Choice(q, disclosed_incorrect3, value=0, label='incorrect3')
    Choice(q, disclosed_correct, value=1, label='correct')
    Validator(q, require)
    
    return comprehension_check(
        [instructions.id], [check.id], next=MakeEstimates, max_attempts=3)
    
# Re-randomize choice order when compiling html
def rerandomize(q):
    q.randomize()
    
# Surprise condition instructions for first estimates
def SurpriseIntro():
    b = Branch(next=MakeEstimates)
    p = Page(b)
    Question(p, surprise_instructions_firstest)
    return b
    
# Surprise condition comprehension check
# create instructions page
# create comprehension check page
# return comprehension check branch
def SurpriseComprehension():
    instructions = Page()
    Question(instructions, surprise_instructions_secondest)
    
    check = Page()
    q = Question(
        check, comprehension_text, qtype='single choice', 
        var='Comprehension', compile=rerandomize, all_rows=True)
    Choice(q, surprise_incorrect1, value=0, label='incorrect1')
    Choice(q, surprise_incorrect2, value=0, label='incorrect2')
    Choice(q, surprise_correct, value=1, label='correct')
    Validator(q, require)
    
    return comprehension_check(
        [instructions.id], [check.id], max_attempts=3)
    
    
    
###############################################################################
# Make estimates
###############################################################################
    
# Make estimates
def MakeEstimates():
    b = Branch(Exit)
    
    # initialize estimate pages
    num_estimates = len(preference_estimate_texts)
    firstest_pages = [Page(b, timer='FirstEstTime') 
        for i in range(num_estimates)]
    secondest_pages = [Page(b, timer='SecondEstTime') 
        for i in range(num_estimates)]
    
    # populate pages with questions
    firstest_question_ids = [preference_estimate(firstest_pages[i].id, i) 
        for i in range(num_estimates)]
    [preference_estimate(secondest_pages[i].id, i, firstest_question_ids[i])
        for i in range(num_estimates)]
    
    # randomize order in which questions appear
    order = list(range(num_estimates))
    shuffle(order)
    
    if g('disclosed'):
        # same questions twice in a row
        for i in order:
            firstest_pages[i].branch(b)
            secondest_pages[i].branch(b)
    else:
        # lists of first and second estimates separated by comprehension check
        # preserve order for first and second estimates
        [firstest_pages[i].branch(b) for i in order]
        firstest_pages[order[-1]].next(SurpriseComprehension)
        [secondest_pages[i].branch(b) for i in order]
        
    return b
    
# Populate preference estimate page with questions
# firstest_id refers to a Question
def preference_estimate(page_id, i, firstest_id=None):
    page = query(page_id, Page)

    q = Question(page,
        '''
        <p>What percent of survey responders {0}?</p>
        <p>(Please type your answer without a '%' sign)</p>
        '''.format(preference_estimate_texts[i]),
        qtype='free', var='FirstEst')
    Validator(q, require)
    Validator(q, integer)
    Validator(q, in_range, {'min':0, 'max':100})
    
    # reminder of first estimate when making second estimate
    # change estimator question variable to SecondEst
    if firstest_id is not None:
        q.var('SecondEst')
        Question(
            page, index=0, compile=remind_firstest, 
            compile_args={'index':i, 'firstest_id':firstest_id})
        Validator(q, different_secondestimate, {'firstest_id':firstest_id})
    
    return q.id
    
# Remind participant of first estimate when making second
# index refers to preference estimate texts list
# firstest_id refers to a Question
def remind_firstest(reminder, index, firstest_id):
    firstest_response = query(firstest_id).get_response()
    reminder.text('''
        <p>You estimated that {0} percent of survey participants {1}.</p>
        <p>We would now like you to guess the answer to this question again, this time giving a different answer than you gave before.</p>
        '''.format(firstest_response, preference_estimate_texts[index]))
        
# Validates that first estimate is different from the second
def different_secondestimate(secondest, firstest_id):
    firstest_response = query(firstest_id).get_response()
    if secondest.get_response() == firstest_response:
        return 'Your second estimate should be different from your first'
       
       
       
###############################################################################
# Exit questions
###############################################################################
       
def Exit():
    b = Branch()
    
    p = Page(b)
    q = Question(
        p, '''
        If you had to bet, which set of your estimates do you think is more accurate on average?''',
        qtype='single choice', var='MoreAccurate', all_rows=True)
    Choice(q, 'The first set', value=1, label='first')
    Choice(q, 'The second set', value=2, label='second')
    q.randomize()
    Validator(q, require)
    
    q = Question(
        p, '''
        Did you try harder to be accurate when making your first or second set of estimates?''', 
        qtype='single choice', var='TryHarder', all_rows=True)
    Choice(q, 'The first set', value=1, label='first')
    Choice(q, 'The second set', value=2, label='second')
    Choice(q, 'I tried equally hard on the first and second set', value=0, label='equal')
    q.randomize()
    Validator(q, require)
    
    p = Page(b)
    q = Question(p, 'Please indicate your gender', 
                 qtype='single choice', var='Gender', all_rows=True)
    Choice(q, 'Male', value=1)
    Choice(q, 'Female', value=0)
    Choice(q, 'Other', value=99)
    Validator(q, require)
    
    q = Question(p, 'How old are you?', qtype='free', var='Age', all_rows=True)
    Validator(q, require)
    Validator(q, integer)
    
    p = Page(b, terminal=True)
    Question(p, 'Thank you for your participation! Your completion code is HL2244')
    
    return b
      
# create the application (survey)
app = create_app(
    Config,
    start=Start,
    password='',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv')
    
# hemlock shell
import hemlock_shell