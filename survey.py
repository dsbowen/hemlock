###############################################################################
# Hemlock survey template
# by Dillon Bowen
# last modified 03/12/2019
###############################################################################

'''
TODO:
clean tools (comp check and randomization)

css - larger margins
'''

# import hemlock package, configuration class, and texts
from hemlock import *
from config import Config
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
    b = Branch()
    p = Page(b)
    Question(p, consent)
    b.next(Free, {'prev_branch_id':b.id})
    return b
    
def Free(prev_branch_id):
    b = query(prev_branch_id, Branch).get_next_branch()
    if b is not None:
        return b

    b = Branch()
    next_args = {}
    
    p = Page(b, timer='free_response_timer', back=True)
    
    Question(p, 
        'For testing purposes, please leave this blank.', 
        qtype='free', var='free response')
    
    q = Question(p)
    q.text('Please enter anything you like in the box')
    q.var('free response')
    q.qtype('free')
    Validator(q, require)
    
    next_args['any'] = q.id
    
    q = Question(p)
    q.text('What is your favorite number?')
    q.var('free response')
    q.qtype('free')
    Validator(q, require)
    Validator(q, integer)
    
    next_args['num'] = q.id
    
    q = Question(p)
    q.text('What is your favorite number between 1000 and 2000?')
    q.var('free response')
    q.qtype('free')
    Validator(q, require)
    Validator(q, integer)
    Validator(q, in_range, {'min':1000,'max':2000})
    
    next_args['big_num'] = q.id
    
    p.randomize()
    
    b.next(FreeNextArgs, next_args)
    
    return b
    
def FreeNextArgs(any, num, big_num):
    any, num, big_num = [query(q).get_response() for q in [any, num, big_num]]
   
    b = Branch(next=SingleChoice)

    p = Page(b, timer='free_next_args_timer', back=True)
    Question(p, '''
    You entered {0} in the free response textbox, your favorite number is {1}, and your favorite number between 1000 and 2000 is {2}
    '''.format(any, num, big_num))
        
    return b
    
def SingleChoice():
    b = Branch(next=Condition)
    
    args = {}
    
    p = Page(b, timer='single_choice_timer', back=True)
    q = Question(p, 'To be, or not to be?', qtype='single choice', var='single_choice')
    Choice(q, text='To be', value=1)
    Choice(q, text='Not to be', value=0)
    Validator(q, require)
    q.randomize()
    
    args['to_be_id'] = q.id
    
    q = Question(p, '''
    Imagine you were suddenly transported to Provence, France, and found yourself in front of a gelateria which sold three flavors gelato. If you could only pick one flavor, what would it be?
    ''')
    q.qtype('single choice')
    q.var('single_choice')
    Choice(q, 'Chocolate')
    Choice(q, 'Lavender')
    Choice(q, 'Orange')
    q.randomize()
    Choice(q, text='I hate ice cream', value='na', label='na')
    Validator(q, require)
    
    args['ice_cream_id'] = q.id
    
    p = Page(
        b, compile=display_choices, compile_args=args, 
        timer='sc_compile_args_timer', back=True)
    
    return b
    
def display_choices(page, to_be_id, ice_cream_id):
    page.clear_questions()

    to_be, ice_cream = [query(qid) for qid in [to_be_id, ice_cream_id]]
    to_be = 'to be' if to_be.get_response() else 'not to be'
    ice_cream = ice_cream.get_data().lower()
        
    if ice_cream == 'na':
        text = '''
        You chose {0}, and for some strange reason you hate ice cream :(
        '''.format(to_be)
    else:
        text = '''
        You chose {0}, and your preferred flavor of ice cream is {1}
        '''.format(to_be, ice_cream)
    Question(page, text)
    
def Condition():
    b = Branch(DispCondition)
    
    c1, c2, c3 = random_assignment(b, 'condition', ['c1','c2','c3'], 
        [[0,1],['low','middle','high'],['up','down','sideways']])
    modg({'c1':c1, 'c2':c2, 'c3':c3})
    
    return b
    
def DispCondition():
    b = Branch()
    
    p = Page(b, timer='disp_condition_timer', back=True)
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
    Validator(q, require, {'message':'''
    That's okay, I have no idea who the characters are either. Just make something up. This isn't English class.
    '''})
    
    p.next(next=Back3, args={'character_id':q.id})
    
    return b
    
def Back3(character_id):
    character = query(character_id).get_response()
    b = Branch()
    
    p = Page(b, back=True, terminal=True)
    Question(p, '''
    I see you like {0}. Personally liked the older brother. {0} was my least favorite character.
    '''.format(character))
    Question(p, '''
    Thank you for taking this survey. If you have any feedback, please email me at dsbowen@wharton.upenn.edu. Your completion code is 'hemlock-test'
    ''')
    
    return b
    
def Start():
    b = Branch()
    p = Page(b, next=Two)
    q = Question(p)
    hello_world(q)
    
    p = Page(b, back=True, next=Six)
    q = Question(p, 'Hello star')
    
    p = Page(b, back=True, terminal=True)
    q = Question(p, 'Hello galaxy')

    return b
    
def hello_world(q):
    q.text('Hello world')
    
def Two():
    b = Branch(next=Three)
    return b
    
def Three():
    b = Branch(next=Four)
    p = Page(b, back=True, next=Five)
    goodbye_world(p)
    return b
    
def goodbye_world(p):
    q = Question(p, 'Goodbye world')
    
def Four():
    b = Branch()
    p = Page(b, back=True)
    q = Question(p, 'Hello moon')
    
    p = Page(b, back=True)
    q = Question(p, 'Goodbye moon')
    
    return b
    
def Five():
    b = Branch()
    return b
    
def Six():
    b = Branch()
    p = Page(b, back=True)
    q = Question(p, 'Goodbye star')
    return b
    
def Test():
    b = Branch()
    
    p1 = Page(b)
    Question(p1, 'Page1')
    p2 = Page(b, back=True)
    Question(p2, 'Page2')
    p3 = Page(b, back=True)
    Question(p3, 'Page3')
    p4 = Page(b, back=True, back_to=p2, terminal=True)
    Question(p4, 'Page4')
    p1.forward_to(p4)
    return b
    
def Start_test():
    instructions1 = Page()
    Question(instructions1, '''I don't know''')
    
    instructions2 = Page()
    Question(instructions2, '''I do now''')
    
    check1 = Page()
    q = Question(check1, '''How many words were in the isntructions?''',
        qtype='free')
    q.post(verify)
    q = Question(check1, '''Yes or no?''', qtype='single choice')
    Choice(q, 'Yes', value=True)
    Choice(q, 'No', value=False)
    
    check2 = Page()
    q = Question(check2, '''Yes, no, or maybe?''', qtype='single choice')
    Choice(q, 'Yes', value=False)
    Choice(q, 'No', value=False)
    q.randomize()
    Choice(q, 'Maybe', value=True)
    
    return comprehension_check(
        [instructions1.id, instructions2.id], [check1.id, check2.id],
        next=End, max_attempts=5)
    
def verify(q):
    response = q.get_response()
    q.data(response == '6')
    
        
def End():
    b = Branch()
    p = Page(b, terminal=True)
    Question(p, 'End of survey')
    return b
      
# create the application (survey)
app = create_app(
    Config,
    start=Start_test,
    password='123',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv')
    
# hemlock shell
import hemlock_shell