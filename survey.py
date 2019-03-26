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
    b = Branch()
    p = Page(b)
    q = Question(p, 'first name', qtype='free', var='name')
    
    p = Page(b)
    q = Question(p, 'last name', qtype='free', var='name')
    
    p = Page(b, terminal=True, back=True)
    q = Question(p, 'terminal')
    
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
