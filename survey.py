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

# import hemlock package, configuration class, and texts
from hemlock import *
from config import Config
from texts import *
from flask_login import current_user

def Start():
    b = Branch()
    p = Page(b)
    q = Question(p, "What's your name?", qtype='free', var='name')
    p = Page(b, terminal=True)
    q = Question(p, 'Hello World')
    return b
      
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