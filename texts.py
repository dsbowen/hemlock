###############################################################################
# Survey texts template
# by Dillon Bowen
# last modified 03/11/2019
###############################################################################

consent = '''

'''

##############################################################################
# Rationality study 0 texts
# by Dillon Bowen
# last modified 07/14/2019
##############################################################################

from copy import deepcopy
from random import choice, shuffle
from numpy import arange

X_INCR = .1
XMIN, XMAX = 1, 5+X_INCR
EXMPL_X = arange(XMIN, XMAX, X_INCR)
TMIN, TMAX = 1, 6
EXMPL_T = arange(TMIN,TMAX,1)

DEF_COLOR = 'limegreen'
ALT_COLOR = 'violet'



##############################################################################
# Stimuli
##############################################################################

# x1, t1, x2, t2
STIMULI = {
    'x1':[0.7, 0.6, 0.8, 1.1, 1.2, 1.5, 2.8, 1.6, 2.1, 1.4],
    'X1':[0.8, 0.7, 0.9, 1.2, 1.3, 1.6, 2.9, 1.7, 2.2, 1.5],
    't1':[1, 1, 2, 3, 3, 1, 2, 1, 3, 1],
    'x2':[1.4, 1.4, 1.3, 1.7, 1.9, 2.1, 3.2, 2.2, 3.0, 2.0],
    'X2':[1.5, 1.5, 1.4, 1.8, 2.0, 2.2, 3.3, 2.3, 3.1, 2.1],
    't2':[3, 5, 4, 4, 5, 4, 4, 5, 5, 3]
    }
# STIMULI = {
    # 'x1':[0.7],
    # 'X1':[0.8],
    # 't1':[1],
    # 'x2':[1.4],
    # 'X2':[1.5],
    # 't2':[3]
    # }
NUM_TRIALS = len(STIMULI['x1'])
STIMULI_VARS = ['x1', 'X1', 't1', 'x2', 'X2', 't2']



##############################################################################
# Consent and main instructions
##############################################################################

consent = '''
<p>We are researchers at the University of Pennsylvania and we are studying decision making. In this survey, you will be asked about your preferences. Please be assured that your responses will be kept completely confidential.</p>
<p>The survey will take you approximately 25 minutes to complete.</p>
<p>Your participation in this research is voluntary. You have the right to withdraw from the study at any point and for any reason without penalty.</p>
<p>We will make every effort to keep all the information you tell us during the study strictly confidential, except as required by law. Your name and other identifying information will never be connected with the responses you provide so no one will ever be able to identify you in any publications that will result from this research. If you have questions about your rights as a volunteer in this research study you can contact the Office of Regulatory Affairs at the University of Pennsylvania at (215)-898-2614.</p>
<p><strong>By continuing with this survey, you acknowledge that you have read the information above and are consenting to participate.</strong></p>
'''

time_preference_instr = '''
<p>This survey will ask you about your 'time preferences'. Specifically, we will ask you about your preferences for winning money (in the form of Amazon Gift Cards) earlier versus later.</p>
'''



##############################################################################
# Intertemporal choice text
##############################################################################

# Both choice options
def get_options_text(x1, t1, x2, t2, color=None):
    return [get_option_text(x, t, color) for x, t, in ((x1, t1), (x2, t2))]

# Choice option
def get_option_text(x, t, color=None):
    try:
        float(x)
        x = '{0:.2f}'.format(x)
    except:
        pass
    opt = option_text.format(x, get_time_text(t))
    if color is None:
        return opt
    return "<span style='color:{0}'>".format(color)+opt+'</span>'

# Time text
def get_time_text(t, color=None):
    if t == 0:
        txt = 'this week'
    elif t == 1:
        txt = 'in {0} week'.format(t)
    else:
        txt = 'in {0} weeks'.format(t)
    if color is None:
        return txt
    return "<span style='color:{0}'>".format(color)+txt+'</span>'

option_text = '${0} Gift Card {1}'

# Get abbreviated intertemporal choice text
def get_ITC_abbr_text(x1, t1, x2, t2, delay_frame):
    if delay_frame:
        x2 = '___'
    else:
        x1 = '___'
    return ITC_abbr_text.format(*get_options_text(x1, t1, x2, t2))
    
ITC_abbr_text = '<p>I am indifferent between receiving a {0} and a {1}.</p>'

# Get intertemporal choice text
# delay_frame indicates that the question is delay framed
# set default x and t, 
# and whether the alternative Gift Card is deliveblue earlier or later
def get_ITC_text(
        x1, t1, x2, t2, delay_frame, def_color=None, alt_color=None):
    if delay_frame:
        GC_def, t_alt, gl = get_option_text(x1, t1, def_color), t2, 'greater'
    else:
        GC_def, t_alt, gl = get_option_text(x2, t2, def_color), t1, 'lesser'
    ITC_abbr = get_ITC_abbr_text(x1, t1, x2, t2, delay_frame)
    t_alt = get_time_text(t_alt, alt_color)
    return ITC_text.format(GC_def, gl, t_alt, ITC_abbr)

# Intertemporal choice text
# Arguments:
# 0: default gift card
# 1: greater or lesser
# 2: alternative timing
# 3: abbreviated intertemporal choice text
ITC_text = '''
<p>Imagine you can either receive a <span style='color:blue'>{0} or a Gift Card of equal or {1} value {2}</span>.</p>
<p>Please fill in the blank below.</p>
{3}
'''
    
    

##############################################################################
# Indifference elicitation comprehension check
##############################################################################
    
# Randomly generate example parameters
def gen_parms():
    exmpl_x, exmpl_t = deepcopy(EXMPL_X), deepcopy(EXMPL_T)
    x1, t1, x2, t2 = [-1]*4
    delay_frame = choice([True, False])
    while x1 > x2 - 3*X_INCR:
        x1, x2 = round(choice(exmpl_x), 2), round(choice(exmpl_x), 2)
    while t1 >= t2:
        t1, t2 = choice(exmpl_t), choice(exmpl_t)
    return x1, t1, x2, t2, delay_frame

def get_indiff_instr_text():
    x1, t1, x2, t2, delay_frame = gen_parms()
    ITC_text = get_ITC_text(x1, t1, x2, t2, delay_frame)
    ans = x2 if delay_frame else x1
    gift_cards = get_options_text(x1, t1, x2, t2)
    implications = get_implications_text(x1, t1, x2, t2)
    return indiff_instr.format(ITC_text, ans, *gift_cards, implications)

# Indifference elicitation instructions
# 0: Intertemporal choice text
# 1: Hypothetical answer
# 2: SS gift card
# 3: LL gift card
# 4: Implications
indiff_instr = '''
<p>Some preference questions will require you to indicate an amount of money such that you would be indifferent between two options.</p>
<p>For example:</p>
{0}
<p><span style='color:blue'>Imagine your answer is ${1:.2f}.</span.</p>
<p>This means you value a {2} as much as a {3}.</p>
<p>This also means that...</p>
<ul>
{4}
</ul>
<p>You may refresh this page for another example.</p>
'''

# Get text for the implications of an indifference announcement
def get_implications_text(x1, t1, x2, t2):
    return '\n'.join([get_implication_text(x1, t1, x2, t2, SS_pref, SS_mod)
        for SS_pref in [True,False] for SS_mod in [True,False]])
    
# Get text for a single implication of an indifference announcement
# SS_pref: indicates SS is preferred to LL
# SS_mod: inicates SS is the modified Gift Card (i.e. SS +/- X_INCR)
def get_implication_text(x1, t1, x2, t2, SS_pref, SS_mod):
    if SS_pref:
        if SS_mod:
            x1 += X_INCR
        else:
            x2 -= X_INCR
    else:
        if SS_mod:
            x1 -= X_INCR
        else:
            x2 += X_INCR
    SS, LL = get_options_text(x1, t1, x2, t2)
    pref, nonpref = (SS,LL) if SS_pref else (LL,SS)
    return implication_text.format(pref, nonpref)
    
# Implications text
# 0: Preferred Gift Card
# 1: Non-preferred Gift Card
implication_text = '''
<li>...you prefer a {0} to a {1}.</li>
'''

# Comprehension intro
comp_intro_text = '''
<p>To be sure you understand the information on the previous page, imagine that you are asked the following question:</p>
'''

# Return indiff comprehension text
def get_indiff_comp_text(x1, t1, x2, t2, delay_frame):
    ITC_text = get_ITC_text(x1, t1, x2, t2, delay_frame)
    x_alt = x2 if delay_frame else x1
    return indiff_comp_hypothetical.format(ITC_text, x_alt)

# Indifference elicitation comprehension check text
indiff_comp_hypothetical = '''
{0}
<p><span style='color:blue'>Imagine you gave an answer of ${1:.2f}.</span></p>
'''

def get_indiff_comp_implication_text(x1, t1, x2, t2):
    return indiff_comp_implication.format(*get_options_text(x1, t1, x2, t2))

# Question for the indiff comprehension check
indiff_comp_implication = '''
<p>Because you are indifferent between receiving a {0} and a {1}, which of the following should you prefer?</p>
'''

# Derive the implication of your hypothetical indiff announcement
# each implication is (preferable option, non-preferable option)
def get_implication_options(x1, t1, x2, t2):
    implications = [
        [x1, t1, x2-X_INCR, t2],
        [x2, t2, x1-X_INCR, t1],
        [x2+X_INCR, t2, x1, t1],
        [x1+X_INCR, t1, x2, t2]]
    implications = [get_options_text(*i) for i in implications]
    shuffle(implications)
    return implications

# Error message if answer is incorrect
indiff_incorrect_text = '''
<p>Your answer to the following question was incorrect. You must answer this question correctly before continuing.</p>
<p>Hint: Think about which of the following options is better or worse than a {0} or a {1}.</p>
<p>You may hit << to reread the instructions.</p>
'''



##############################################################################
# Payment comprehension check
##############################################################################

payment_instr = '''
<p>We will ask you time preference questions using both free responses and multiple choice questions. Sometimes, a question may be repeated. When this happens, your answer may be the same as, or different from, your original answer.</p>
<p><span style='color:blue'>You will receive an Amazon Gift Card based on one of your answers, which will be selected at random. If you answer the same question multiple times, your Gift Card may be based on any of your answers.</span></p>
'''

bonus_comp = '''
Please indicate how your Gift Card will be determined.
'''

bonus_choices = [
    'I will receive a Gift Card based on one of my answers, which will be selected at random',
    'I will receive a Gift Card for every question I answer',
    'I will receive a Gift Card for two or more of my answers, which will be selected at random'
    ]
    
repeats_comp = '''
Please indicate what happens if you answer the same question multiple times.
'''

repeats_choices = [
    'My Gift Card may be based on any of my answers',
    'My Gift Card may be based on my original answer, but not on any subsequent answers',
    'My Gift Card may be based on my last answer, but not on any previous answers'
    ]
    
    
    
##############################################################################
# Mechanism comprehension check
##############################################################################

incentive_compatibility_instr = '''
<p>If your Gift Card is based on a multiple choice question, you will receive the option you selected.</p>
<p>If your Gift Card is based on a free response question, your Gift Card will be determined using an <i>incentive compatile mechanism</i>. <span style='color:blue'>This means there is no way to 'game the system' to achieve a better outcome. You will be best off when you respond truthfully.</span></p>
'''

def get_mech_instr():
    x1, t1, x2, t2, delay_frame = gen_parms()
    ITC_text = get_ITC_text(x1, t1, x2, t2, delay_frame)
    ans = x2 if delay_frame else x1
    mech_exmpls = get_mech_exmpls(x1, t1, x2, t2, delay_frame)
    return mech_instr.format(ITC_text, ans, mech_exmpls)
    
mech_instr = '''
<p>To understand how this mechanism works, imagine you are asked the following question:</p>
<p>***</p>
{0}
<p>***</p>
<p><span style='color:blue'>Imagine your answer is ${1:.2f}</span>.</p>
<p>The computer will then fill in the blank with its own dollar amount. This amount will determine the Gift Card you will potentially receive for this trial.</p>
<p>Here is how this works.</p>
{2}
<p>You may refresh this page for another example.</p>
'''

def get_mech_exmpls(x1, t1, x2, t2, delay_frame):
    return '\n'.join([get_mech_exmpl(x1, t1, x2, t2, delay_frame, winX)
        for winX in [True,False]])

# Get mechanism example text
# determine human answer
# determine computer answer
# determine earlier and later, preferred and nonpreferred Gift Cards
def get_mech_exmpl(x1, t1, x2, t2, delay_frame, winX):
    ans = x2 if delay_frame else x1
    
    if delay_frame and winX:
        xmin, xmax = x2+X_INCR, XMAX+X_INCR
    elif not delay_frame and not winX:
        xmin, xmax = XMIN-X_INCR, x1-X_INCR
    else:
        xmin, xmax = x1+X_INCR, x2-X_INCR
    comp_ans = choice(arange(xmin, xmax, X_INCR))
    
    if delay_frame:
        GC1, GC2 = get_options_text(x1, t1, comp_ans, t2)
        prefGC, nonprefGC = (GC2, GC1) if winX else (GC1, GC2)
    else:
        GC1, GC2 = get_options_text(comp_ans, t1, x2, t2)
        prefGC, nonprefGC = (GC1, GC2) if winX else (GC2, GC1)
        
    return mech_exmpl.format(comp_ans, GC1, GC2, ans, prefGC)

mech_exmpl = '''
<p>Imagine the computer randomly fills in ${0:.2f}. This means you are effectively offered a choice between a {1} and a {2}. Your answer of ${3:.2f} implies that you prefer the {4}, so that is what you would receive if this trial were selected.</p>
'''

def get_mech_exmpl_text():
    x1, t1, x2, t2, delay_frame = gen_parms()
    ITC_text = get_ITC_text(x1, t1, x2, t2, delay_frame, DEF_COLOR, ALT_COLOR)
    SS, LL = get_options_text(x1, t1, x2, t2, DEF_COLOR)
    ans, GC_def, t_alt = (x2, SS, t2) if delay_frame else (x1, LL, t1)
    GC_alt = get_option_text('X', t_alt)
    t_alt = get_time_text(t_alt, ALT_COLOR)
    return mech_exmpl.format(ITC_text, GC_def, t_alt, ans)

mech_comp = '''
<span style='color:blue'>Imagine you answer ${0:.2f} and the computer randomly fills in ${1:.2f}</span>. Which Gift Card do you receive?
'''

mech_incorrect_text = '''
<p>Your answer to the following question was incorrect. You must answer this question correctly before continuing.</p>
<p>You may hit << to reread the instructions.</p>
'''



##############################################################################
# Main survey
##############################################################################

main_intro_text = 'You are about to continue to the main part of the survey'

def get_outcome_text(X, actGC):
    return outcome_text.format(X, actGC)

outcome_text = '''
<p>The computer filled in ${0:.2f}, giving you a {1}.</p>
'''

def get_counterfactual_texts(x_hat, X, actGC, cfGC):
    if X < x_hat:
        act_gl, cf_gl = 'greater than or equal to', 'less than'
    else:
        act_gl, cf_gl = 'less than', 'greater than or equal to'
    cf_text = counterfactual_text.format(cf_gl, X, cfGC)
    actGC_long = act_long.format(actGC, act_gl, X)
    cfGC_long = cf_long.format(cfGC, cf_gl, X)
    return cf_text, actGC_long, cfGC_long
    
counterfactual_text = '''
<p><span style='color:blue'>If your answer had been {0} than ${1:.2f}, you would have won a {2} instead.</span></p>
<p>Which do you prefer?</p>
'''
   
act_long = '''
{0}. This is the Gift Card you won because your answer was {1} ${2:.2f}
'''
   
cf_long = '''
{0}. This is the Gift Card you would have won if your answer had been {1}  ${2:.2f}
'''

def get_revise_text(stimulus, delay_frame):
    return revise_text.format(get_ITC_abbr_text(*stimulus, delay_frame))
    
revise_text = '''
<p>Consider the same question again:</p>
{0}
'''

def get_recall_text(CF, x_hat, X):
    if not CF:
        return ''
    higher_lower = 'lower' if X < x_hat else 'higher'
    return recall_text.format(higher_lower)
        
recall_text = '''
<p><span style='color:blue'>The last time you answered a similar question, you said you would prefer the Gift Card you would have won if your answer had been {0}.</style></p>
'''

exit_text = '''
Thank you for your participation! Based on one of your answers, we will email you a ${0:.2f} Amazon Gift Card {1}.
'''