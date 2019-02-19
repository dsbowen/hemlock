

preference_estimate_texts = [
    ' would rather have the superpower of flight than super strength',
    ' would prefer mushrooms over LSD if they had to take a psychadelic',
    ' own crypto currency',
    ' believe Dick Cheney will go to heaven when he dies',
    ' would trade in their car for a self driving car of otherwise comparable quality',
    ' would prefer execution over life in prison if convicted of first degree murder in Texas',
    ' believe Nancy Pelosi is more similar to George Washington than Donald Trump',
    ' expect the world to end after 2100',
    ' know who invented the computer',
    ' can juggle'
    ]

preference_question_texts = [
    'Which superpower would you prefer?',
    'If you had to take a psychadelic, which would you prefer?',
    'Do you own crypto currency?',
    'Do you believe Dick Cheney will go to heaven when he dies?',
    'If you could trade in your car for a self driving car of otherwise comparable quality, would you do it?',
    'If you were convicted of first degree murder in Texas, which sentence would you prefer?',
    'Who do you believe is more similar to George Washington?',
    'When do you expect the world to end?',
    'Do you know who invented the computer?',
    'Can you juggle?'
    ]
    
preference_options = [
    ('Super strength', 'Flight'),
    ('LSD', 'Mushrooms'),
    ('No', 'Yes'),
    ('No', 'Yes'),
    ('No', 'Yes'),
    ('Life in prison', 'Execution'),
    ('Donald Trump', 'Nancy Pelosi'),
    ('Before 2100', 'After 2100'),
    ('No','Yes'),
    ('No','Yes')
    ]

consent = '''
<p>We are researchers at the University of Pennsylvania and we are studying decision making. In this survey, you will be asked to make some estimates. Please be assured that your responses will be kept completely confidential.</p>
<p>The survey will take you approximately 10 minutes to complete. For completing this survey, you will be compensated $1 by MTurk.</p>
<p>Your participation in this research is voluntary. You have the right to withdraw from the study at any point and for any reason without penalty.</p>
<p>We will make every effort to keep all the information you tell us during the study strictly confidential, except as required by law. Your name and other identifying information will never be connected with the responses you provide so no one will ever be able to identify you in any publications that will result from this research. If you have questions about your rights as a volunteer in this research study you can contact the Office of Regulatory Affairs at the University of Pennsylvania at (215)-898-2614.</p>
<p><strong>By continuing with this survey, you acknowledge that you have read the information above and are consenting to participate.</strong></p>
'''

intro_preferences = '''
On the next page, we will ask you some questions about your behaviors and preferences. Please answer them honestly. Your responses will be confidential.
'''
    
first_est_intro_surprise = '''
<p>On the next pages, we will ask you to estimate the experiences and preferences of all survey participants.</p>
<p>You should do your best to be accurate. For each question, you will receive a bonus of $0.25 if your estimate is correct.</p>
<p>You will receive your bonus via MTurk within one week of completing this survey.</p>
'''

second_est_intro_surprise = '''
<p>On the next pages, we will ask you to estimate the experiences and preferences of all survey participants again.</p>
<p>Your second estimate must be different from your first estimate.</p>
<p><strong>This will give you a second chance to make correct estimates, and thus a second chance to earn a bonus.</strong> You will win a bonus of $0.20 if your second estimate is correct. That is, for each question, you will receive a bonus of $0.25 if your first estimate is correct, and a bonus of $0.20 if your second estimate is correct.</span></p>
<p>You will receive your bonus via MTurk within one week of completing this survey.</p>
'''

first_est_intro_disclosed = '''
<p>On the next pages, we will ask you to estimate the experiences and preferences of all survey participants.&nbsp;</p>
<p><strong>For each of the questions, we will ask you to make two estimates in a row.</strong> Your second estimate must be different from your first estimate.</p>
<p>You should do your best to be accurate. For each question, you will receive a bonus of $0.25 if your first estimate is correct, or $0.20 if your second estimate is correct.</p>
<p><strong>Since you will be making two estimates for each question, this will give you two chances to make correct estimates, and thus two chances to win a bonus.</strong></p>
<p>You will receive your bonus via MTurk within one week of completing this survey.</p>
'''