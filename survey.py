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
# Charitable giving survey
# idea by Katie Mehr
# coded by Dillon Bowen
# last modified 03/28/2019
###############################################################################

# import hemlock package, configuration class, and texts
from hemlock import *
from config import Config
from texts import *
from flask_login import current_user
from datetime import datetime, timedelta
import re

MAX_DONORS = 100



###############################################################################
# Assign to donor or recruiter condition
###############################################################################

# Assign to donor or recruiter condition
def AssignCondition():
    b = Branch(Consent)
    
    set_timed_out()
    
    donor_ids = [p.id for p in Participant.query.all() 
        if p.g('donor') and not p.g('timed_out')]
    eligible_donor_ids = get_eligible_donors(donor_ids)
    if not eligible_donor_ids:
        if len(donor_ids) >= MAX_DONORS:
            b.next(AtCapacity)
            return b
        modg({'matched_recruiter_id':None})
        donor = 1
    else:
        create_match(eligible_donor_ids[0])
        Question(
            branch=b, data=g('matched_donor_donation'), var='donation')
        donor = 0

    modg({'donor':donor})
    q = Question(branch=b, qtype='embedded', data=donor, var='donor')
    
    return b
    
# set the timed out global variable for participants
def set_timed_out():
    incomplete = [p for p in Participant.query.all() 
        if not p.get_metadata()['completed']]
    [i.modg({'timed_out':get_timed_out(i)}) for i in incomplete]
    
# Return an indicator that the participant has timed out
def get_timed_out(part):
    running_time = datetime.utcnow() - part.get_metadata()['start_time']
    return running_time > timedelta(hours=1)
    
# Return a list of eligible donors
# i.e. participants who are donors, who have not timed out,
#   and have not been assigned to a recruiter
# first unmatch donors from recruiters who have timed out
# then return list of eligible donors
# Note: donor_ids are ids of donors who have not timed out
def get_eligible_donors(donor_ids):
    donors = query(donor_ids, Participant)
    matched_donors = [d for d in donors
        if d.g('matched_recruiter_id') is not None]
    [d.modg({'matched_recruiter_id':None}) for d in matched_donors
        if query(d.g('matched_recruiter_id'), Participant).g('timed_out')]
        
    return [d.id for d in donors if
        (d.get_metadata()['completed'] 
        and d.g('matched_recruiter_id') is None)]
    
# Return a message if survey has reached its capacity of donors
# and there are no more eligible donors to assign to recruiters
def AtCapacity():
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(
        p, '''
        <p>Our records indicate that our survey has reached its capacity of participants.</p>
        <p>Thank you for your continuing interest in our research.</p>
        ''')
    return b
    
# Create a match between recruiter (current participant) and matched donor
def create_match(matched_donor_id):
    matched_donor = query(matched_donor_id, Participant)
    modg({'matched_donor_id':matched_donor.id})
    matched_donor.modg({'matched_recruiter_id':current_user.id})
    
    donation = matched_donor.g('donation')
    modg({'matched_donor_donation':donation})
    



###############################################################################
# Begin survey
###############################################################################

# Consent and MTurk ID
def Consent():
    b = Branch(next=Name)
    p = Page(b)
    q = Question(p, consent)
    q = Question(
        p, 'Please enter your MTurk ID', 
        qtype='free', var='workerId', all_rows=True)
    Validator(q, require)
    return b
    
# Ask for initials of an acquaintance
def Name():
    b = Branch()
    p = Page(b)
    q = Question(
        p, acquaintance_text, 
        qtype='free', var='initials', all_rows=True)
    Validator(q, require)
    Validator(q, max_letters)
    
    modg({'initials_id':q.id})
    
    b.next(ConsiderSituation)
    
    return b
    
# Initials contain a maximum of 3 characters
def max_letters(q):
    initials = q.get_response()
    if len(initials) > 3:
        return 'Enter no more than three letters for the initials'
    
# Participants consider a situation involving their acquaintance   
def ConsiderSituation():
    modg({'initials':query(g('initials_id')).get_response()})

    b = Branch(Scenarios)
    p = Page(b)
    q = Question(p, situation_text.format(g('initials')))
        
    return b
    
# Donation scenarios
def Scenarios():
    b = Branch()
    
    p = Page(b)
    if g('donor'):
        q = Question(p, donor_scenario.format(g('initials')))
        b.next(MakeDonation)
    else:
        q = Question(
            p, recruiter_scenario.format(
                g('initials'), g('matched_donor_donation')))
        b.next(DVs)
        
    return b
    
# Donors decide to make a donation
# then imagine how they would feel after making this donation
def MakeDonation():
    b = Branch(DVs)
    p = Page(b)
    donation = Question(p, elicit_donation_text, qtype='free', var='donation')
    Validator(donation, require)
    Validator(donation, decimals_exact, {'decimals':2})
    message = 'Your donation should be at least $0.00'
    Validator(donation, minimum, {'min':0.0, 'message':message})
    
    p = Page(b)
    q = Question(
        p, 
        compile=add_imagine_donation_text, 
        compile_args={'donation_id':donation.id})
    
    return b
    
def number(q, message=None):
    data = q.get_data()
    if data is None or data == '':
        return
        
    if re.match("^(-)?\d+\.\d+$", data) is not None:
        return
    if message is not None:
        return message
    return "Please enter a number"
    
def minimum(q, min, message=None):
    data = q.get_data()
    if data is None or data == '':
        return

    try:
        data = type(min)(data)
    except:
        return 'Please enter the correct type of data'
        
    if min <= data:
        return
        
    if message is not None:
        return message
    return 'Your answer should be greater than {0}'.format(min)
    
def decimals_exact(q, decimals, message=None):
    data = q.get_data()
    if data is None or data == '':
        return
        
    if re.match("^(-)?\d+\.\d{%d}$" % decimals, data) is not None:
        return
    if message is not None:
        return message
    return "Please enter a number with exactly two decimal places"
    
# Add imagine donation text to imagine donation question
def add_imagine_donation_text(q, donation_id):
    donation = query(donation_id).get_response()
    modg({'donation':donation})
    q.text(imagine_donation_text.format(donation))
    
# Collect DVs
# set the question texts and DV variable names (condition specific)
# add pages to collect DVs
def DVs():
    b = Branch(Demographics)
    
    if g('donor'):
        question_texts = donor_dvs_question
        dvs_var = donor_dvs_var
    else:
        question_texts = recruiter_dvs_question
        dvs_var = recruiter_dvs_var
    
    for i in range(len(question_texts)):
        p = Page(b)
        q = Question(
            p, donor_dvs_question[i].format(g('initials')),
            qtype='single choice', var=dvs_var[i])
        Validator(q, require)
        for i in range(11):
            c = Choice(q, text=str(i))
            if i == 0:
                c.text(str(i)+' Not at all true')
            if i == 10:
                c.text(str(i)+' Extremely True')
            c.value(i)
            c.label(str(i))
    b.randomize()
    return b
    
# Collect demographics
def Demographics():
    b = Branch(AttentionCheck)
    p = Page(b)
    
    q = Question(p, 'What is your age?', qtype='free', var='age')
    Validator(q, require)
    Validator(q, integer)
    Validator(q, in_range, {'min':18,'max':105})
    
    q = Question(p, 'What is your gender?', qtype='single choice', var='gender')
    Choice(q, 'Male', value=1)
    Choice(q, 'Female', value=2)
    Choice(q, 'Other', value=3)
    Validator(q, require)
    
    q = Question(p, 'What is your race?', qtype='single choice', var='race')
    for i in range(len(race)):
        Choice(q, race[i], value=i)
    Validator(q, require)
        
    q = Question(
        p, 'How much money do you donate to charity each year?',
        qtype='free', var='normalDonation')
    Validator(q, require)
    Validator(q, integer)
    
    q = Question(p, importance_text, qtype='single choice', var='importance')
    for i in range(len(importance_level)):
        Choice(q, importance_level[i], value=i+1)
    Validator(q, require)
    
    return b
    
# Attention check and completion page
def AttentionCheck():
    b = Branch()
    p = Page(b)
    q = Question(p, attention_check_text, qtype='single choice', var='attention')
    for i in range(len(attention_choices_text)):
        c = Choice(q, attention_choices_text[i], value=0)
        if i == 0:
            c.value(1)
    q.randomize()
    Validator(q, require)
    
    p = Page(b, terminal=True)
    q = Question(p, completion_code)
    
    return b
      
# create the application (survey)
app = create_app(
    Config,
    start=AssignCondition,
    password=password,
    record_incomplete=True,
    block_duplicate_ips=False,
    block_from_csv='block.csv')
    
# hemlock shell
import hemlock_shell
