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
    treatment = random_assignment(b, 'treat', ['Treatment'], [[0,1]])
    
    p = Page(b)
    q = Question(p, "Choose 'yes' to at most 3")
    yn_qid = [create_yn_question(p) for i in range(5)]
    Validator(q, max_yesses, args={'max_y':3, 'yn_qid': yn_qid})
    
    p = Page(b)
    q = Question(p)
    if treatment:
        q.text("<p>You are in the treatment condition, which means you can go back.</p>")
        p.back()
    else:
        q.text("<p>You are in the control condition, which means you can never go back!</p>")
    
    p = Page(b, terminal=True)
    q = Question(p, 'Thank you for participanting!')
    return b
    
def create_yn_question(page):
    q = Question(
        page, 'Yes or no?', qtype='single choice', var='YN')
    Choice(q, 'Yes', value=1)
    Choice(q, 'No', value=0)
    return q.id
    
def max_yesses(q, max_y, yn_qid):
    yn_questions = query(yn_qid)
    values = [yn.get_data() for yn in yn_questions]
    if sum(values) > max_y:
        return "<p>You answered 'yes' to {} questions.</p>".format(sum(values))
      
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
