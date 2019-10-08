"""Hemlock survey"""

from hemlock import *
from texts import *

from flask_login import current_user
from random import shuffle

def Start(root=None):
    b = Branch()
    
    p = Page(b, submit_worker=True)
    q = Text(p, text="""
    <p>This page has a "submit worker".</p>
    <p>That means all functions which execute after the form has been validated are sent to the redis queue. For example, you might want to feed the submitted data to an ML model and re-estimate the parameters before the next page. However, the validation functions themselves are executed before the RQ starts, allowing for quick page validation.</p>
    <p>For example, you need to answer 'yes' to the question below. Try answering 'no' first.</p>
    """)
    force_yes_question(p)

    p = Page(b, validator_worker=True)
    q = Text(p, text="""
    <p>Pretty sweet loading page, huh?</p>
    <p>Okay, not really, it's more like a placeholder for when I get my logo gif.</p>
    <p>Anyway, so the loading page renders any time a worker is called. The loading page has some javascript which connects a socket. The socket listens on a unique namespace dedicated to the current page. When it hears 'job finished', it continues the program.</p> 
    """)
    q = Text(p, text="""
    <p>Okay, so now you're thinking, 'But Dillon, sometimes validation functions take a super long time to run! How will I ever execute a long-running validation function if I can only provision the worker for submit functions??'</p>
    <p>Not to fear!</p>
    <p>I have graciously provided the option to allocate a validator worker as well.</p>
    <p>This page provisions a worker for validation. Try answering 'no' to the question and see what happens.</p>
    """)
    force_yes_question(p)

    p = Page(b)
    q = Text(p, text="""
    <p>You can also provision 'compile workers', which handle all the functions which execute as the page is compiling.</p>
    <p>Notice the loading page before the next screen.</p>
    """)

    p = Page(b, compile_worker=True)
    q = Text(p, text="""
    <p>Try reloading the page and notice the compile worker running again.</p>
    <p>You'll also see the choices below re-randomized each time.</p>
    """)
    ice_cream_question(p)

    p = Page(b, cache_compile=True, compile_worker=True)
    q = Text(p, text="""
    <p>Alright, so that's not so bad for a short compile function like re-randomizing the choices.</p>
    <p>But let's say we've got a compile function that takes a super long time to run. You've just gotten onto the next screen and...</p>
    <p>OMG YOU ACCIDENTALLY HIT THE REFRESH BUTTON AND NOW IT'S GOING TO TAKE ANOTHER 2 MINUTES TO RELOAD THE PAGE!!!</p>.
    <p>Caching to the rescue!</p>
    <p>You can add a 'cache' option to the compile worker so that it only runs the compile function once.</p>
    <p>This page had a compile worker with the caching option activated. Try reloading it and see what (doesn't) happen.</p>
    """)
    ice_cream_question(p)

    p = Page(b, compile_worker=True, validator_worker=True, submit_worker=True)
    q = Text(p, text="""
    <p>Okay, last thing for now.</p>
    <p>You can also mix and match the workers. This page has all three: a compile worker, validator worker, and submit worker.</p>
    <p>Check out the console (ctrl+shift+j for me) to see the socket listening in on the RQ.</p>
    <p>After you click the next arrow, see if you can notice the socket connecting, the job starting, and the job finishing twice.</p>
    <p>It's not a bug; it's because the page calls two workers after it's posted: one for validation and one for submission.</p>
    """)
    
    p = Page(b, terminal=True)
    q = Text(p, text='Goodbye World!')
    return b

def force_yes_question(page):
    q = SingleChoice(page, text="""
    <p>Please answer 'yes' to this question.</p>
    """)
    Choice(q, text="Yes", value=1)
    Choice(q, text="No", value=0)
    Validator(q, force_yes)

def force_yes(question):
    if question.response is None or not question.response.value:
        return "<p>I THOUGHT I TOLD YOU TO ANSWER YES!!!</p>"

def ice_cream_question(page):
    q = MultiChoice(page, text="<p>Which of these ice cream flavors do you like?</p>")
    Choice(q, text="Chocolate")
    Choice(q, text="Vanilla")
    Choice(q, text="Lavender")
    Choice(q, text="Orange")
    CompileFunction(q, rerandomize)

def rerandomize(question):
    shuffle(question.choices)