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

'''
# import hemlock package, configuration class, and texts
from hemlock import *
from debug import AIParticipant as AIP
from config import Config
from texts import *
from flask_login import current_user

def Start():
    b = Branch()
    p = Page(b, debug=AIP.debug_test, debug_attrs={'test':'hello moon'})
    q = Question(p, '<p>hello moon</p>')
    q = Question(p, '<p>hello world</p>', qtype='free')
    Validator(q, require)
    p = Page(b)
    q = Question(
        p, '<p>goodbye world</p>', qtype='free', 
        debug=AIP.debug_test2, debug_args={'hello':'world'})
    Validator(q, require)
    p = Page(b)
    q = Question(
        p, '<p>What is your favorite ice cream flavor?</p>', 
        qtype='single choice')
    Choice(q, 'Lavender', debug=AIP.debug_test3)
    Choice(q, 'Chocolate')
    Choice(q, 'Orange')
    Validator(q, require)
    p = Page(b, terminal=True)
    q = Question(p, '<p>goodbye galaxy</p>')
    return b 
      
# create the application (survey)
app = create_app(
    Config,
    start=Start,
    password='',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv',
    debug=True)
    
# run app
if __name__ == '__main__':
    app.run()
    
# hemlock shell
import hemlock_shell
'''

# import hemlock package, configuration class, and texts
from hemlock import *
from debug import AIParticipant as AIP
from config import Config
from texts import *
from flask_login import current_user

def Start():
    b = Branch()
    p = Page(b)
    q = Question(p, '<p>hello moon</p>')
    q = Question(p, '<p>hello world</p>', qtype='free')
    Validator(q, require)
    p = Page(b)
    q = Question(p, '<p>goodbye world</p>', qtype='free')
    Validator(q, require)
    p = Page(b)
    q = Question(
        p, '<p>What is your favorite ice cream flavor?</p>', 
        qtype='single choice')
    Choice(q, 'Lavender')
    Choice(q, 'Chocolate')
    Choice(q, 'Orange')
    Validator(q, require)
    p = Page(b, terminal=True)
    q = Question(p, '<p>goodbye galaxy</p>')
    return b 
      
# create the application (survey)
app = create_app(
    Config,
    start=Start,
    password='',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv',
    debug=True)
    
# run app
if __name__ == '__main__':
    app.run()
    
# hemlock shell
import hemlock_shell