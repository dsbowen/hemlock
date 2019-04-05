###############################################################################
# Survey texts template
# by Dillon Bowen
# last modified 03/11/2019
###############################################################################

consent = '''

'''

###############################################################################
# Second guesses study 7 - confidence texts
# by Dillon Bowen
# last modified 03/30/2019
###############################################################################



###############################################################################
# Preference questions
###############################################################################
preference_estimate_elicitation = '''
<p>What percent of survey responders {0}?</p>
<p>Please enter your answer with a '%' sign.</p>
'''

reminder_text = '''
<p>You estimated that {0} percent of survey participants {1}.</p>
<p>We would now like you to guess the answer to this question again, this time giving a different answer than you gave before.</p>
'''

indicate_better_text = '''
<p>We asked you to estimate what percent of survey responders {0}. You gave the following estimates:</p>
<p>First estimate: {1}%</p>
<p>Second estimate: {2}%</p>
<p>Which would you prefer?</p>
'''

firstest_better_text = '''
$0.30 bonus if my first estimate is correct and $0.20 bonus if my second estimate is correct
'''
secondest_better_text = '''
$0.20 bonus if my first estimate is correct and $0.30 bonus if my second estimate is correct
'''

# preference_estimate_texts = [
    # ' would rather have the superpower of flight than super strength',
    # ' believe it should be legal to use psychedelic drugs  (e.g. LSD)',
    # ' own crypto currency (e.g. Bitcoin)',
    # ' would prefer Dick Cheney over Sarah Palin to be president of the United States',
    # ' would feel safer in a self-driving car (rather than driving themselves)',
    # ' would rather spend their evening going to a play at the theater than seeing a movie',
    # ' prefer red over blue',
    # ' believe climate change is a serious threat to human survival',
    # " are more curious to try Soap flavored Bertie Bott's Every Flavour Beans than Earthworm flavored Bertie Bott's Every Flavour Beans",
    # ' can juggle with 3 balls'
    # ]

# preference_question_texts = [
    # 'Which superpower would you prefer?',
    # 'Do you believe it should be legal to use psychedelic drugs (e.g. LSD)?',
    # 'Do you own crypto currency (e.g. Bitcoin)?',
    # 'Who would you prefer to have as president of the United States of America?',
    # 'Would you feel safer driving in a self-driving car?',
    # 'How would you rather spend your evening?',
    # 'Which color do you prefer?',
    # 'Do you believe climate change is a serious threat to human survival?',
    # "Which flavor of Bertie Bott's Every Flavour Beans would you be more curious to try?",
    # 'Can you juggle with 3 balls?'
    # ]
    
# preference_options = [
    # ('Super strength', 'Flight'),
    # ('No', 'Yes'),
    # ('No', 'Yes'),
    # ('Sarah Palin', 'Dick Cheney'),
    # ('I would feel safer driving myself', 'I would feel safer in a self-driving car'),
    # ('Seeing a movie', 'Going to a play at the theater'),
    # ('Blue', 'Red'),
    # ('No', 'Yes'),
    # ('Earthworm', 'Soap'),
    # ('No','Yes')
    # ]
    
preference_estimate_texts = [
    ' would rather have the superpower of flight than super strength',
    ' believe it should be legal to use psychedelic drugs  (e.g. LSD)'
    ]

preference_question_texts = [
    'Which superpower would you prefer?',
    'Do you believe it should be legal to use psychedelic drugs (e.g. LSD)?'
    ]
    
preference_options = [
    ('Super strength', 'Flight'),
    ('No', 'Yes')
    ]



###############################################################################
# Consent and introductory instructions
###############################################################################

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
    
    
    
###############################################################################
# First estimate instructions
###############################################################################

firstest_instructions = '''
<p>On the next pages, we will ask you to estimate the experiences and preferences of all survey participants.</p>
<p>You should do your best to be accurate. For each question, you will receive a bonus of $0.20 if your estimate is correct.</p>
<p>You will receive your bonus via MTurk within one week of completing this survey.</p>
'''



###############################################################################
# Second estimate instructions
###############################################################################

secondest_instructions = '''
<p>On the next pages, we will ask you to estimate the experiences and preferences of all survey participants again.</p>
<p>Your second estimate must be different from your first estimate.</p>
<p>This will give you a second chance to make correct estimates, and thus a second chance to earn a bonus. That is, for each question, you will receive a $0.20 bonus if either of your estimates is correct.</p>
<p>You will receive your bonus via MTurk within one week of completing this survey.</p>
'''

comprehension_text = '''
To be sure you have read and understood the instructions, please indicate how your bonus will be determined
'''

secondest_correct = '''
For each question, I will receive a $0.20 bonus if either my first or second estimate is correct
'''
secondest_incorrect1 = '''
For each question, I will receive a $0.20 bonus only if my first estimate (the estimate I just gave) was correct
'''
secondest_incorrect2 = '''
For each question, I will receive a $0.20 bonus only if my second estimate (the estimate I am about to give) is correct
'''



###############################################################################
# Indicate better estimate instructions
###############################################################################

indicate_better_instructions = '''
<p>On the next pages, we will ask you to indicate whether you think your first or second estimate is more likely to be correct. You will do this by choosing whether to add $0.10 to the bonus you will receive if your first estimate is correct, or to the bonus you will receive if your second estimate is correct.</p>
<p>If you choose to add $0.10 to the bonus you will receive if your first estimate is correct, you will receive a $0.30 bonus if your first estimate is correct and a $0.20 bonus if your second estimate is correct.</p>
<p>If you choose to add $0.10 to the bonus you will receive if your second estimate is correct, you will receive a $0.20 bonus if your first estimate is correct and a $0.30 bonus if your second estimate is correct.
'''

indicate_better_correct = '''
I will choose whether to add $0.10 to the bonus for my first or second estimate. That is, I will choose whether to receive $0.30 if my first estimate is correct and $0.20 if my second estimate is correct, or $0.20 if my first estimate is correct and $0.30 if my second estimate is correct.
'''
indicate_better_incorrect1 = '''
$0.10 will be added to my bonus if my first estimate is correct. That is, I will receive $0.30 if my first estimate is correct and $0.20 if my second estimate is correct.
'''
indicate_better_incorrect2 = '''
$0.10 will be added to my bonus if my second estimate is correct. That is, I will receive $0.20 if my first estimate is correct and $0.30 if my second estimate is correct.
'''



###############################################################################
# Completion code
###############################################################################

completion = 'Thank you for your participation! Your completion code is HL2357'
