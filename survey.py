##############################################################################
# Hemlock survey template
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

# import hemlock package, configuration class, and texts
from hemlock import *
from custom_compilers import *
from debug import AIParticipant as AIP
from config import Config
from texts import *
from flask_login import current_user

def Start():
    raise NotImplementedError()
    
def Start():
    b = Branch()
    p = Page(b)
    city = Question(
        p, "Where is your next vacation?", qtype='free', var='City')
    Validator(city, require)
    dessert = Question(
        p, "What's your favorite dessert?", qtype='single choice', 
        var='Dessert')
    Choice(dessert, 'Cake')
    Choice(dessert, 'Ice cream')
    Choice(dessert, 'Cannoli')
    dessert.randomize()
    Validator(dessert, require)
    
    b.next(End, args={'city': city, 'dessert': dessert})
    return b
    
def End(city, dessert):
    city = city.get_response()
    dessert = dessert.get_response()
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, "Your vacation is to {0} and your favorite dessert is {1}".format(city, dessert))
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
