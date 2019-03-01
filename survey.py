###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/27/2019
###############################################################################

'''
TODO:
general cleaning, incl routes folder and relationships (as opposed to queries)
for debugging, pass args to start function
back for branch embedded dataframe
record empty dataframe
vaidation bank
css - larger margins
page needs all_rows
also timer function
next branch id stuff not working
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

def Dropdown():
    b = Branch()
    p = Page(b)
    q = Question(p, 'hello world')
    q.qtype('dropdown')
    Choice(q, 'hello world')
    Choice(q, 'hello moon')
    Choice(q, 'hello star')
    return b

def Consent():
    b = Branch(Free)
    p = Page(b)
    Question(p, consent)
    return b
    
def Free():
    b = Branch(FreeNextArgs)
    next_args = {}
    
    p = Page(b, timer='free_response_timer')
    
    Question(p, 'For testing purposes, please leave this blank.', 'free', 'free response')
    
    q = Question(p)
    q.text('Please enter anything you like in the box')
    q.var('free response')
    q.qtype('free')
    Validator(q, require)
    
    next_args['anything'] = q.id
    
    q = Question(p)
    q.text('What is your favorite number?')
    q.var('free response')
    q.qtype('free')
    Validator(q, require)
    Validator(q, integer)
    
    next_args['favorite_number'] = q.id
    
    q = Question(p)
    q.text('What is your favorite number between 1000 and 2000?')
    q.var('free response')
    q.qtype('free')
    Validator(q, require)
    Validator(q, integer)
    Validator(q, in_range, [1000,2000])
    
    next_args['favorite_number_inrange'] = q.id
    
    p.randomize()
    
    b.next(args=next_args)
    
    return b
    
def FreeNextArgs(free_responses):
    free_responses = query(free_responses)
    
    b = Branch(SingleChoice)
    p = Page(b, timer='free_next_args_timer')
    Question(p, '''
    You entered {0} in the free response textbox, your favorite number is {1}, and your favorite number between 1000 and 2000 is {2}
    '''.format(
        free_responses['anything'].get_response(),
        free_responses['favorite_number'].get_response(),
        free_responses['favorite_number_inrange'].get_response()))
        
    return b
    
def SingleChoice():
    b = Branch(Condition)
    
    args = {}
    
    p = Page(b, timer='single_choice_timer')
    q = Question(p, 'To be, or not to be?', 'single choice', 'single_choice')
    Choice(q, 'To be', 1)
    Choice(q, 'Not to be', 0)
    Validator(q, require)
    q.randomize()
    
    args['to_be'] = q.id
    
    q = Question(p, '''
    Imagine you were suddenly transported to Provence, France, and found yourself in front of a gelateria which sold three flavors gelato. If you could only pick one flavor, what would it be?
    ''')
    q.qtype('single choice')
    q.var('single_choice')
    Choice(q, 'Chocolate')
    Choice(q, 'Lavender')
    Choice(q, 'Orange')
    q.randomize()
    Choice(q, 'I hate ice cream', 'na', label='na')
    Validator(q, require)
    
    args['ice_cream'] = q.id
    
    p = Page(b, render=display_choices, render_args=args, timer='sc_render_args_timer')
    
    return b
    
def display_choices(page, args):
    args = query(args)
    to_be = 'not to be'
    if args['to_be'].get_data():
        to_be = 'to be'
    if args['ice_cream'].get_data() == 'na':
        text = '''
        You chose {0}, and for some strange reason you hate ice cream :(
        '''.format(to_be)
    else:
        text = '''
        You chose {0}, and your preferred flavor of ice cream is {1}
        '''.format(to_be, args['ice_cream'].get_response().lower())
    Question(page, text)
    
def Condition():
    b = Branch(DispCondition)
    
    c1, c2, c3 = random_assignment(b, 'condition', ['c1','c2','c3'], 
        [[0,1],['low','middle','high'],['up','down','sideways']])
    modg({'c1':c1, 'c2':c2, 'c3':c3})
    
    return b
    
def DispCondition():
    b = Branch()
    
    p = Page(b, timer='disp_condition_timer')
    Question(p, '''
    <p>We have just randomly assigned you to the conditions {0}, {1}, and {2}.</p>
    <p>(This is completely meaningless, just continue to the next page!)</p>
    '''.format(g('c1'), g('c2'), g('c3')))
    
    p.next(Back1)
    
    return b

def Back1():
    b = Branch(Back2)
    
    p = Page(b, timer='back')
    Question(p, '''
    <p>These next pages are designed to test the back button</p>
    <p>Feel free to click back and forward as you like to see if anything breaks :)</p>
    ''')
    p.back()
    
    return b
    
def Back2():        
    b = Branch()
    
    p = Page(b, timer='back', back=True)
    q = Question(p, '''
    Who is your favorite character from Fyodor Dostoevsky's The Brothers Karamazov?
    ''')
    q.qtype('free')
    q.var('favorite_character')
    q.all_rows()
    Validator(q, require, '''
    That's okay, I have no idea who the characters are either. Just make something up. This isn't English class.
    ''')
    
    p.next(Back3, q.id)
    
    return b
    
def Back3(character):
    character = query(character).get_response()
    b = Branch()
    
    p = Page(b, back=True, terminal=True)
    Question(p, '''
    I see you like {0}. Personally liked the older brother. {0} was my least favorite character.
    '''.format(character))
    Question(p, '''
    Thank you for taking this survey. If you have any feedback, please email me at dsbowen@wharton.upenn.edu. Your completion code is 'hemlock-test'
    ''')
    
    return b
        
app = create_app(Config, 
    start=Dropdown, 
    password='hemlock-test235711',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'restore_branch':restore_branch, 'even_randomize':even_randomize, 'random_assignment':random_assignment,'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np, 'Randomizer':Randomizer}