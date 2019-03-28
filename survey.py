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

def Start():
    b = Branch(End)
    p = Page(b)
    q = Question(p, 'Hello world')
    return b
    
def End():
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, 'Goodbye world')
    return b
      
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