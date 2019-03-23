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

# import hemlock package, configuration class, and texts
from hemlock import *
from config import Config
from texts import *
from flask_login import current_user

def Start():
    b = Branch(End)
    p = Page(b)
    q = Question(p, 'First name', qtype='free', var='name')
    q = Question(p, 'Last name', qtype='free', var='name')
    
    return b
    
def End():
    b = Branch()
    p = Page(b, back=True, terminal=True)
    q = Question(p, 'End')
    return b 
      
# create the application (survey)
app = create_app(
    Config,
    start=Start,
    password='',
    record_incomplete=True,
    block_duplicate_ips=False,
    block_from_csv='block.csv')
    
# hemlock shell
import hemlock_shell