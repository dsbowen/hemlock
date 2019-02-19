###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/19/2019
###############################################################################

'''
TODO:
general cleaning, incl routes folder and relationships (as opposed to queries)
for debugging, pass args to start function
back for branch embedded dataframe
record empty dataframe
vaidation bank
css - larger margins
'''

from hemlock import create_app, db, query, restore_branch, even_randomize, random_assignment, modg, g, comprehension_check, Participant, Branch, Page, Question, Choice, Validator, Variable, Randomizer
from hemlock.validation_bank import *
from config import Config
import pandas as pd
import numpy as np
from random import choice, shuffle
from copy import deepcopy
from flask_login import current_user

from texts import *

def Consent():
    b = Branch(next=IntroPreferences)
    p = Page(b)
    q = Question(p, consent)
    q = Question(p, 'Enter your MTurk ID:', 'free', 'workerId', all_rows=True)
    Validator(q, require)
    return b
    
def IntroPreferences():
    b = Branch()
    
    [Question(branch=b, qtype='embedded', var='preference_label', data=text)
        for text in preference_estimate_texts]
    
    disclosed = random_assignment(b, 'condition', ['disclosed'], [[0,1]])
    modg({'disclosed':disclosed})
    
    p = Page(b)
    q = Question(p, intro_preferences)
    
    p = Page(b)
    [create_preference_question(p.id, i) 
        for i in range(len(preference_question_texts))]
    p.randomize()
    
    if g('disclosed'):
        b.next(DisclosedComprehension)
    else:
        b.next(SurpriseIntro)
    
    return b
        
def create_preference_question(page_id, i):
    page = query(page_id, Page)
    q = Question(page, preference_question_texts[i], 'single choice', var='preference')
    Choice(q, preference_options[i][1], 1, 'yes')
    Choice(q, preference_options[i][0], 0, 'no')
    Validator(q, require)
    q.randomize()
    
def DisclosedComprehension():        
    instructions = Page()
    Question(instructions, first_est_intro_disclosed)
    
    check = Page()
    q = Question(check, qtype='single choice', var='Comprehension', all_rows=True)
    q.render(reset, check.id)
    q.text('''
        To be sure you have read and understood the instructions, please indicate how your bonus will be determined''')
    Choice(q, '''
        I will make one estimate for each question. I will receive a bonus if this estimate is correct.''', 0, 'incorrect1')
    Choice(q, '''
        I will make two estimates for each question. I will receive a bonus only if the first estimate is correct.''', 0, 'incorrect2')
    Choice(q, '''
        I will make two estimates for each question. I will receive a bonus only if the second estimate is correct''', 0, 'incorrect3')
    Choice(q, '''
        I will make two estimates for each question. I will receive a bonus if either estimate is correct''', 1, 'correct')
    Validator(q, require)
    
    return comprehension_check(instructions.id, check.id, MakeEstimates, max_attempts=3)
    
def SurpriseIntro():
    b = Branch(next=MakeEstimates)
    p = Page(b)
    Question(p, first_est_intro_surprise)
    return b
    
def SurpriseComprehension():
    instructions = Page()
    Question(instructions, second_est_intro_surprise)
    
    check = Page()
    q = Question(check, qtype='single choice', var='Comprehension', all_rows=True)
    q.render(reset, check.id)
    q.text('''
        To be sure you have read and understood the instructions, please indicate how your bonus will be determined''')
    Choice(q, '''
        For each question, I will receive a bonus only if my first estimate (the estimate I just gave) was correct.''', 0, 'incorrect1')
    Choice(q, '''
        For each question, I will receive a bonus only if my second estimate (the estimate I am about to give) is correct''', 0, 'incorrect2')
    Choice(q, '''
        For each question, I will receive a a bonus if either my first or second estimate is correct''', 1, 'correct')
    Validator(q, require)
    
    return comprehension_check(instructions.id, check.id, max_attempts=3)
    
def reset(q, check_id):
    check = query(check_id, Page)
    if check._direction_to == 'invalid':
        return
    q.reset_default()
    q.clear_error()
    q.randomize()
    
def MakeEstimates():
    b = Branch(Exit)
    
    # initialize estimate pages
    num_estimates = len(preference_estimate_texts)
    first_est_pages = [Page(b) for i in range(num_estimates)]
    second_est_pages = [Page(b) for i in range(num_estimates)]
    
    # populate pages with questions
    first_est_question_ids = [preference_estimate(first_est_pages[i].id, i) 
        for i in range(num_estimates)]
    [preference_estimate(second_est_pages[i].id, i, first_est_question_ids[i])
        for i in range(num_estimates)]
    
    # randomize order in which questions appear
    order = list(range(num_estimates))
    shuffle(order)
    
    if g('disclosed'):
        for i in order:
            first_est_pages[i].branch(b)
            second_est_pages[i].branch(b)
    else:
        [first_est_pages[i].branch(b) for i in order]
        first_est_pages[order[-1]].next(SurpriseComprehension)
        [second_est_pages[i].branch(b) for i in order]
        
    return b
    
def preference_estimate(page_id, i, first_est_id=None):
    page = query(page_id, Page)

    q = Question(page,
        'What percent of survey responders {0}?'.format(preference_estimate_texts[i]),
        'free', 'FirstEst')
    Validator(q, require)
    Validator(q, integer)
    Validator(q, in_range, [0,100])
    
    # page changes for second estimate
    if first_est_id is not None:
        Question(page, order=0,
            render=remind_first_est, render_args=[i, first_est_id])
        q.var('SecondEst')
        Validator(q, different_second_estimate, first_est_id)
    
    return q.id
    
def remind_first_est(reminder, args):
    i, first_est_id = args
    first_est = query(first_est_id)
    first_est_response = first_est.get_response()
    reminder.text('''
        <p>You estimated that {0} percent of survey participants {1}.</p>
        <p>We would now like you to guess the answer to this question again, this time giving a different answer than you gave before.</p>
        '''.format(first_est_response, preference_estimate_texts[i]))
        
def different_second_estimate(second_est, first_est_id):
    first_est = query(first_est_id)
    if second_est.get_response() == first_est.get_response():
        return 'Your second estimate should be different from your first'
        
def Exit():
    b = Branch()
    
    p = Page(b)
    q = Question(p, 'If you had to bet, which set of your estimates do you think is more accurate on average?', 'single choice', 'MoreAccurate', all_rows=True)
    Choice(q, 'The first set', 1, 'first')
    Choice(q, 'The second set', 2, 'second')
    q.randomize()
    Validator(q, require)
    
    q = Question(p, 'Did you try harder to be accurate when making your first or second set of estimates?', 'single choice', 'TryHarder', all_rows=True)
    Choice(q, 'The first set', 1, 'first')
    Choice(q, 'The second set', 2, 'second')
    Choice(q, 'I tried equally hard on the first and second set', 0, 'equal')
    q.randomize()
    Validator(q, require)
    
    p = Page(b)
    q = Question(p, 'Please indicate your gender', 'single choice', 'Gender', all_rows=True)
    Choice(q, 'Male', 1)
    Choice(q, 'Female', 0)
    Choice(q, 'Other', 99)
    Validator(q, require)
    
    q = Question(p, 'How old are you?', 'free', 'Age', all_rows=True)
    Validator(q, require)
    
    p = Page(b, terminal=True)
    Question(p, 'Thank you for your participation! Your completion code is xxxx')
    
    return b
        
app = create_app(Config, 
    start=Consent, 
    password='123',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'restore_branch':restore_branch, 'even_randomize':even_randomize, 'random_assignment':random_assignment,'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np, 'Randomizer':Randomizer}