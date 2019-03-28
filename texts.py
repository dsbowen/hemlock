###############################################################################
# Survey texts template
# by Dillon Bowen
# last modified 03/11/2019
###############################################################################

consent = '''

'''

###############################################################################
# Survey texts
# by Katie Mehr
# coded by Dillon Bowen
# last modified 03/28/2019
###############################################################################

consent = '''
CONSENT
'''

acquaintance_text = '''
INITIALS_ASK
'''

situation_text = '''
<p>For this scenario, we will ask you to consider a situation with you and the person you mentioned; <span style="color: #0000ff;">{0}</span></p>
<p>Click next to continue</p>
'''

donor_scenario = '''
DONOR SCENARIO
<span style="color: #0000ff;">{0}</span>
'''

# to pipe in initials, use <span style="color: #0000ff;">{0}</span>
# to pipe in amount, use <span style="color: #ff0000;">{1}</span>
recruiter_scenario = '''
RECRUITER_SCENARIO
<span style="color: #0000ff;">{0}</span>
<span style="color: #ff0000;">{1}</span>
'''

elicit_donation_text = '''
ELICIT_DONATION
'''

imagine_donation_text = '''
IMAGINE DONATION
<span style="color: #ff0000;">{0}</span>
'''

donor_dvs_question = [
'1 <span style="color: #0000ff;">{0}</span>',
'2 <span style="color: #0000ff;">{0}</span>',
'3 <span style="color: #0000ff;">{0}</span>',
'4 <span style="color: #0000ff;">{0}</span>',
'5 <span style="color: #0000ff;">{0}</span>',
'6 <span style="color: #0000ff;">{0}</span>',
'7 <span style="color: #0000ff;">{0}</span>']

donor_dvs_var = [
'v1',
'v2',
'v3',
'v4',
'v5',
'v6',
'v7']

recruiter_dvs_question = [
'1 <span style="color: #0000ff;">{0}</span>',
'2 <span style="color: #0000ff;">{0}</span>']

recruiter_dvs_var = [
'v1_r',
'v2_r']

race = [
'race1',
'race2',
'etc']

importance_text = '''
IMPORTANCE TEXT
'''

importance_level = [
'not at all', 
'etc']

attention_check_text = '''
ATTENTION CHECK
'''

attention_choices_text = [
'correct',
'incorrect',
'also incorrect']

completion_code = '''
COMPLETION CODE
'''

password = ''