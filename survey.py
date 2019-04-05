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
from flask_login import current_user

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
# Second guesses confidence study 1
# by Dillon Bowen
# last modified 04/04/2019
###############################################################################

# import hemlock package, configuration class, and texts
from hemlock import *
from config import Config
from texts import *
from flask_login import current_user
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
    b = Branch(FirstEstInstructions)
    
    # add preference labels as embedded data
    [Question(branch=b, qtype='embedded', var='preference_label', data=text)
        for text in preference_estimate_texts]
    
    # preference instructions
    p = Page(b)
    q = Question(p, intro_preferences)
    
    # add multiple choice questions to page to indicate preferences
    p = Page(b, timer='PreferencesTime', all_rows=True)
    [create_preference_question(p.id, i) 
        for i in range(len(preference_question_texts))]
    p.randomize()
    
    return b
        
# Create a preference indication question and add to page
def create_preference_question(page_id, i):
    page = query(page_id, Page)
    q = Question(
        page, preference_question_texts[i], 
        qtype='single choice', var='Preference')
    Choice(q, preference_options[i][1], value=1, label='yes')
    Choice(q, preference_options[i][0], value=0, label='no')
    q.randomize()
    Validator(q, require)
    
    

###############################################################################
# First estimates
###############################################################################

def FirstEstInstructions():
    b = Branch(FirstEstimates)
    p = Page(b)
    q = Question(p, firstest_instructions)
    return b
    
# Make first estimates
def FirstEstimates():
    b = Branch(SecondEstInstructions)
    
    # randomize order of estimates
    estorder = list(range(len(preference_estimate_texts)))
    shuffle(estorder)
    modg({'estorder':estorder})
    
    # create first estimate pages
    firstest_pages = []
    firstest_qids = []
    for text in preference_estimate_texts:
        p = Page(part=current_user, timer='FirstEstTime')
        firstest_pages.append(p)
        
        # elicit first estimate
        qid = create_estimate_question(p.id, text, 'FirstEst')
        firstest_qids.append(qid)
    
    # store ids of first estimate questions
    modg({'firstest_qids':firstest_qids})
    
    # assign first estimate pages to branch in order estorder
    [firstest_pages[i].branch(b) for i in estorder]

    return b
    
# create an estimate question
def create_estimate_question(pid, text, var):
    p = query(pid, Page)
    q = Question(
            p, preference_estimate_elicitation.format(text), 
            qtype='free', var=var)
    Validator(q, require)
    Validator(q, integer)
    Validator(q, isin, {'interval':('[',0,100,']')})
    return q.id
    
    
    
###############################################################################
# Second estimates
###############################################################################

# Second estimate instructions and comprehension check
def SecondEstInstructions():
    instructions = Page()
    q = Question(instructions, secondest_instructions)
    
    check = Page()
    q = Question(
        check, comprehension_text, 
        qtype='single choice', var='secondest_comprehension',
        compile=rerandomize, all_rows=True)
    Choice(q, secondest_correct, value=1, label='secondest_correct')
    Choice(q, secondest_incorrect1, value=0, label='secondest_incorrect1')
    Choice(q, secondest_incorrect2, value=0, label='secondest_incorrect2')
    Validator(q, require)
    
    return comprehension_check(
        [instructions.id], [check.id], max_attempts=3, next=SecondEstimates)
        
# Re-randomize choices for comprehension check question on compile
def rerandomize(q):
    q.randomize()
    
# Make second estimates
def SecondEstimates():
    b = Branch(IndicateBetterInstructions)
    
    # retrieve first estimates
    firstests = [q.get_response() for q in query(g('firstest_qids'))]
    
    # create second estimate pages
    secondest_pages = []
    secondest_qids = []
    for text, firstest in zip(preference_estimate_texts,  firstests):
        p = Page(part=current_user, timer='SecondEstTime')
        secondest_pages.append(p)
        
        # remider of first estimate
        q = Question(p, reminder_text.format(firstest, text))
        
        # elicit second estimate
        qid = create_estimate_question(p.id, text, 'SecondEst')            
        secondest_qids.append(qid)
        Validator(query(qid), different_secondest, {'firstest':firstest})
        
    # store ids of second estimate questions
    modg({'secondest_qids':secondest_qids})
    
    # assign second estimate pages to branch in order estorder
    [secondest_pages[i].branch(b) for i in g('estorder')]
    
    return b
    
# Validate that the second estimate is different from the first
def different_secondest(q, firstest):
    if q.get_response() == firstest:
        return 'Your second estimate should be different from your first'
    
    
    
###############################################################################
# Indicate better estimate
###############################################################################

# Indicate better instructions and comprehension check
def IndicateBetterInstructions():
    instructions = Page()
    q = Question(instructions, indicate_better_instructions)
    
    check = Page()
    q = Question(
        check, comprehension_text, 
        qtype='single choice', var='indicate_better_comprehension',
        compile=rerandomize, all_rows=True)
    Choice(q, indicate_better_correct, value=1, label='indicate_better_correct')
    Choice(q, indicate_better_incorrect1, value=0, label='indicate_better_incorrect1')
    Choice(q, indicate_better_incorrect2, value=0, label='indicate_better_incorrect2')
    Validator(q, require)
    
    return comprehension_check(
        [instructions.id], [check.id], max_attempts=3, next=IndicateBetter)

# Indicate which estimate is better
def IndicateBetter():
    b = Branch(ExitQuestions)
    
    # retrieve first and second estimates
    firstests = [q.get_response() for q in query(g('firstest_qids'))]
    secondests = [q.get_response() for q in query(g('secondest_qids'))]
    tuples = zip(preference_estimate_texts, firstests, secondests)
    
    # create pages to indicate whether the first or second estimate was better
    indicate_better_pages = []
    for text, firstest, secondest in tuples:
        p = Page(part=current_user, timer='IndicateBetterTime')
        indicate_better_pages.append(p)
        
        q = Question(
            p, indicate_better_text.format(text, firstest, secondest),
            qtype='single choice', var='SecondEstBetter')
        Choice(q, firstest_better_text, value=0, label='firstest')
        Choice(q, secondest_better_text, value=1, label='secondest')
        Validator(q, require)
        
    # add pages to branch in order estorder
    [indicate_better_pages[i].branch(b) for i in g('estorder')]
        
    return b



###############################################################################
# Exit questions
###############################################################################
       
def ExitQuestions():
    b = Branch(End)
    
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
    
    return b
    
def End():
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, completion)
    return b
      
# create the application (survey)
app = create_app(
    Config,
    start=Start,
    password='',
    record_incomplete=True,
    block_duplicate_ips=False,
    block_from_csv='block.csv')
    
# hemlock shell
import hemlock_shell