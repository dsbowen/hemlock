##############################################################################
# Hemlock survey template
# by Dillon Bowen
# last modified 04/29/2019
##############################################################################
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
    
# run app
if __name__ == '__main__':
    app.run()
    
# hemlock shell
import hemlock_shell
'''
##############################################################################
# Rationality study 0
# by Dillon Bowen
# last modified 07/14/2019
##############################################################################

# import hemlock package, configuration class, and texts
from hemlock import *
from config import Config
from texts import *
from flask_login import current_user

def Start():
    b = Branch(next=IndifferenceComprehension)
    p = Page(b)
    q = Question(p, consent)
    q = Question(
        p, 'Please enter your Lab ID', 
        qtype='free', var='LabID', all_rows=True)
    Validator(q, require)
    
    p = Page(b)
    q = Question(p, time_preference_instr)
    return b



##############################################################################
# Indifference elicitation comprehension check
##############################################################################
    
# Indifference comprehension check navigation function
def IndifferenceComprehension():
    b = Branch(next=PaymentComprehension)
    
    p = Page(b)
    q = Question(p, compile=gen_indiff_instr)
    
    # comp = [gen_indiff_comp_page(p, df) for df in [True,False]]
    # shuffle(comp)
    # [c.branch(b) for c in comp]
    comp = gen_indiff_comp_page(p, choice([True,False]))
    comp.branch(b)
    
    return b
    
# Randomly generage example to use in instructions
def gen_indiff_instr(q):
    q.text(get_indiff_instr_text())
    
# Randomly generates indifference comprehension page
def gen_indiff_comp_page(page, delay_frame):
    p = Page(
        back=True, back_to=page, 
        timer='IndiffCompTimer_df'+str(int(delay_frame)), all_rows=True,
        compile=set_forward_to, compile_args={'prev_page_id':page.id})
    q = Question(p, comp_intro_text)
    
    x1, t1, x2, t2, _ = gen_parms()
    q = Question(p, get_indiff_comp_text(x1,t1,x2,t2,delay_frame))
    
    implications = get_implication_options(x1, t1, x2, t2)
    stimulus = [x1, t1, x2, t2, delay_frame]
    comp_questions = [gen_indiff_comp_question(*stimulus, i) 
        for i in implications]
    shuffle(comp_questions)
    [q.page(p) for q in comp_questions]
    
    return p
    
# Set this as the page after the instructions page
# to avoid repeating comprehension pages
def set_forward_to(p, prev_page_id):
    query(prev_page_id, Page).forward_to(p)
    
# Generate an indifference comprehension question
def gen_indiff_comp_question(x1, t1, x2, t2, delay_frame, implication):
    x_hat = x2 if delay_frame else x1
    text = get_indiff_comp_implication_text(x1, t1, x2, t2)
    q = Question(text=text, qtype='single choice')
    Choice(q, implication[0], value=1)
    Choice(q, implication[1], value=0)
    q.randomize()
    Validator(q, require)
    Validator(q, indiff_correct, args={'x1':x1,'t1':t1,'x2':x2,'t2':t2})
    return q
    
# Validate the indifference comprehension answer is correct
def indiff_correct(q, x1, t1, x2, t2):
    if q.get_data():
        return
    return indiff_incorrect_text.format(*get_options_text(x1, t1, x2, t2))



##############################################################################
# Payment comprehension check
##############################################################################

# Payment comprehension check
def PaymentComprehension():
    instr = Page()
    q = Question(instr, payment_instr)
    
    comp = Page()
    gen_payment_comp_question(comp.id, bonus_comp, bonus_choices)
    gen_payment_comp_question(comp.id, repeats_comp, repeats_choices)
    
    return comprehension_check(
        [instr.id], [comp.id], max_attempts=3, next=MechanismComprehension)
    
# Generate a payment comprehension question
# The first choice is always correct (value 1)
# but order will be randomized on compile
def gen_payment_comp_question(comp_id, text, choices):
    q = Question(
        query(comp_id, Page), text, 
        qtype='single choice', compile=rerandomize)
    [Choice(q, c, value=0) for c in choices]
    q.get_choices()[0].value(1)
    Validator(q, require)
    
# Rerandomize choices on compile
def rerandomize(q):
    q.randomize()



##############################################################################
# Mechanism comprehension check
##############################################################################

# Mechanism comprehension branch
def MechanismComprehension():
    b = Branch(next=MainIntro)
    
    p = Page(b)
    q = Question(p, incentive_compatibility_instr)
    
    p = Page(b)
    q = Question(p, compile=gen_mech_exmpl)
    
    comp = [gen_mech_comp_page(p, df) for df in [True,False]]
    shuffle(comp)
    [c.branch(b) for c in comp]
    
    return b
    
# Randomly generage example of the mechanism to use in instructions
def gen_mech_exmpl(q):
    q.text(get_mech_instr())
    
# Randomly generates a mechanism comprehension page
def gen_mech_comp_page(page, delay_frame):
    p = Page(
        back=True, back_to=page, 
        timer='MechCompTimer_df'+str(int(delay_frame)), all_rows=True,
        compile=set_forward_to, compile_args={'prev_page_id':page.id})
    q = Question(p, comp_intro_text)
        
    x1, t1, x2, t2, _ = gen_parms()
    q = Question(p, get_ITC_text(x1, t1, x2, t2, delay_frame))
    
    comp_questions = [gen_mech_comp_question(x1,t1,x2,t2,delay_frame,winX)
        for winX in [True,False]]
    shuffle(comp_questions)
    [q.page(p) for q in comp_questions]
    
    return p
    
# Generate mechanism comprehension check question
def gen_mech_comp_question(x1, t1, x2, t2, delay_frame, winX):
    q = Question(qtype='single choice')
    choices = [Choice(q, value=0) for i in range(4)]
    
    X, x_alt = -1, -1
    if delay_frame:
        exmpl_x = arange(x1, XMAX, X_INCR)
        if winX:
            while not (x1 < x_alt < X):
                X, x_alt = choice(exmpl_x), choice(exmpl_x)
            choices[0].value(1)
        else:
            while not (x1 < X < x_alt):
                X, x_alt = choice(exmpl_x), choice(exmpl_x)
            choices[1].value(1)
        choice_text_parms = [(X, t2), (x1, t1), (X, t1), (x_alt, t2)]
    else:
        exmpl_x = arange(XMIN, x2, X_INCR)
        if winX:
            while not (x_alt < X < x2):
                X, x_alt = choice(exmpl_x), choice(exmpl_x)
            choices[2].value(1)
        else:
            while not (X < x_alt < x2):
                X, x_alt = choice(exmpl_x), choice(exmpl_x)
            choices[3].value(1)
        choice_text_parms = [(X, t2), (x_alt, t1), (X, t1), (x2, t2)]
        
    [c.text(get_option_text(*parm), reset_value=False)
        for c, parm in zip(choices, choice_text_parms)]
    
    q.text(mech_comp.format(x_alt, X))
    q.randomize()
    Validator(q, require)
    Validator(q, mech_correct)
    return q
    
# Validates the answer to the mechanism comprehension check is correct
def mech_correct(q):
    if q.get_data():
        return
    return mech_incorrect_text



##############################################################################
# Main survey
##############################################################################

# Introduction to the main survey
# randomly assign to feedback or no feedback condition
# randomly order trials
def MainIntro():
    b = Branch(next=Main, next_args={'round':0})
    p = Page(b)
    q = Question(p, main_intro_text)
    modg({'feedback':random_assignment(b, 'feedback', ['Feedback'], [[0,1]])})
    order = list(range(NUM_TRIALS))
    shuffle(order)
    modg({'trial_order':order})
    return b

# Main survey branch
# branch contains one trial 
# i.e. pair of delay- and speedup-frame question sets
def Main(round):
    b = Branch()
    b.next(Exit) if round == NUM_TRIALS-1 else b.next(Main, {'round':round+1})
    
    record_stimulus(b.id, round)
    trial = [gen_trial_page(round==0, df) for df in [True,False]]
    shuffle(trial)
    [page.branch(b) for page in trial]
    
    return b
    
# Record stimulus for this trial in 1) global, 2) dataset
def record_stimulus(branch_id, round):
    b = query(branch_id, Branch)
    Question(branch=b, data=round, var='Round')
    trial = g('trial_order')[round]
    Question(branch=b, data=trial, var='Trial')
    [Question(branch=b, data=STIMULI[v][trial], var=v) for v in STIMULI_VARS]
    modg({v:STIMULI[v][trial] for v in STIMULI_VARS})
    
# Generate trial page
# add recall feedback if feedback condition
# if feedback condition, add branch to Feedback
# else, calculate original bonus in post function
def gen_trial_page(first_round, delay_frame):
    p = Page(timer='TrialTimer_df'+str(int(delay_frame)))
    stimulus = g(['x1','t1','x2','t2'])
    ITC_text = get_ITC_text(*stimulus, delay_frame)
    if not first_round and g('feedback'):
        if delay_frame:
            ITC_text += get_recall_text(*g(['CF_d','x2_hat','X2']))
        else:
            ITC_text += get_recall_text(*g(['CF_s','x1_hat','X1']))
    q = Question(p, ITC_text, qtype='free')
    q.var('x2_hat') if delay_frame else q.var('x1_hat')
    Validator(q, require)
    Validator(q, numeric)
    
    if g('feedback'):
        p.next(Feedback, {'original_qid':q.id, 'delay_frame':delay_frame}) 
    else:
        q.post(original_bonus, {'delay_frame':delay_frame})

    return p
    
# Feedback branch
# outcome feedback
# counterfactual reasoning
# revision
def Feedback(original_qid, delay_frame):
    x_hat, X, actGC, cfGC = original_bonus(query(original_qid), delay_frame)
    
    b = Branch()
    p = Page(
        b, timer='FeedbackTimer_df'+str(int(delay_frame)),
        post=feedback_bonus, post_args={'delay_frame':delay_frame})
    
    q = Question(p, get_outcome_text(X, actGC))
    cf_text, actGC_long, cfGC_long = get_counterfactual_texts(
        x_hat, X, actGC, cfGC)
        
    q = Question(p, cf_text, qtype='single choice')
    q.var('CF_d') if delay_frame else q.var('CF_s')
    Choice(q, actGC_long, label='Actual', value=0)
    Choice(q, cfGC_long, label='Counterfactual', value=1)
    Validator(q, require)
    
    revise_text = get_revise_text(g(['x1','t1','x2','t2']), delay_frame)
    q = Question(p, revise_text, qtype='free')
    q.var('x2_hat_r') if delay_frame else q.var('x1_hat_r')
    Validator(q, require)
    Validator(q, numeric)
    
    return b
    
# Calculates the original bonus
# i.e. bonus based on original announcement
def original_bonus(original, delay_frame):
    try:
        x_hat = float(original.get_data())
    except:
        return
    if g('feedback'):   
        X = g('X2') if delay_frame else g('X1')
    else:
        X = round(choice(deepcopy(EXMPL_X))/2, 2)
    
    if delay_frame:
        actGC, cfGC = calculate_bonus(*g(['x1','t1','t2']), X, x_hat)
    else:
        actGC, cfGC = calculate_bonus(*g(['x2','t2','t1']), X, x_hat)
    
    if delay_frame:
        modg({'x2_hat':x_hat, 'actGC_d':actGC, 'cfGC_d':cfGC})
    else:
        modg({'x1_hat':x_hat, 'actGC_s':actGC, 'cfGC_s':cfGC})
    return x_hat, X, actGC, cfGC
    
# Calculate feedback bonus
# i.e. bonuses based on counterfactual reasoning and revised announcements
def feedback_bonus(p, delay_frame):
    CF, x_hat_r = [q.get_data() for q in p.get_questions()[1:3]]
    try:
        x_hat_r = float(x_hat_r)
    except:
        return
        
    if CF:
        modg({'bonus':g('bonus')+[g('cf_bonus')]})
    else:
        modg({'bonus':g('bonus')+[g('bonus')[-1]]})
        
    X = round(choice(deepcopy(EXMPL_X))/2, 2)
    if delay_frame:
        modg({'CF_d':CF})
        calculate_bonus(*g(['x1','t1','t2']), X, x_hat_r)
    else:
        modg({'CF_s':CF})
        calculate_bonus(*g(['x2','t2','t1']), X, x_hat_r)

# Calculates a bonus
# x_def, t_def amount and timing of default Gift Card
# t_alt alternative schedule
def calculate_bonus(x_def, t_def, t_alt, X, x_hat):
    if X < x_hat:
        bonus, timing, cf_bonus, cf_timing = x_def, t_def, X, t_alt
    else:
        bonus, timing, cf_bonus, cf_timing = X, t_alt, x_def, t_def
    actGC = get_option_text(bonus, timing)
    cfGC = get_option_text(cf_bonus, cf_timing)
    
    if g('bonus') is None:
        modg({'bonus':[(bonus, timing)]})
    else:
        modg({'bonus':g('bonus')+[(bonus, timing)]})
    modg({'cf_bonus':(cf_bonus, cf_timing)})
        
    return actGC, cfGC
    
        

        
##############################################################################
# Exit questions
##############################################################################

def Exit():
    b = Branch(End)
    p = Page(b)
    q = Question(
        p, 'Please indicate your gender', qtype='single choice', 
        var='Gender', all_rows=True)
    Choice(q, 'Male', value=1)
    Choice(q, 'Female', value=0)
    Choice(q, 'Other', value=99)
    Validator(q, require)
    q = Question(
        p, 'Please enter your age', qtype='free', var='Age', all_rows=True)
    Validator(q, require)
    Validator(q, integer)
    return b

def End():
    b = Branch()
    bonus, timing = choice(g('bonus'))
    Question(branch=b, data=bonus, var='Bonus', all_rows=True)
    Question(branch=b, data=timing, var='Timing', all_rows=True)
    p = Page(b, terminal=True)
    q = Question(p, exit_text.format(bonus, get_time_text(timing)))
    return b
      
# create the application (survey)
app = create_app(
    Config,
    start=Start,
    password='r@tional',
    record_incomplete=True,
    block_duplicate_ips=False,
    block_from_csv='block.csv')
    
# run app
if __name__ == '__main__':
    app.run()
    
# hemlock shell
import hemlock_shell