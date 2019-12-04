from hemlock import *

BALL_BAT_TXT = """
<p>A bat and ball cost $1.10 in total. The bat costs $1.00 more than the ball.</p>
<p>How much does the ball cost?</p>
"""

def create_ball_bat_q():
    ball_bat_q = Free(prepend='$', text=BALL_BAT_TXT)
    Validate(ball_bat_q, require)
    Validate(ball_bat_q, numeric)
    Submit(ball_bat_q, data_to_float)
    return ball_bat_q

ball_bat = {
    'var': 'CRT.BallBat',
    'create_question': create_ball_bat_q,
    'answer': {
        'correct': .05,
        'intuitive': .10
    }
}

MACHINES_TXT = """
<p>If it takes 5 machines 5 minutes to make 5 widgets, how many minutes would it take 100 machines to make 100 widgets?
"""

def create_machines_q():
    machines_q = Free(text=MACHINES_TXT, append='minutes')
    Validate(machines_q, require)
    Validate(machines_q, numeric)
    Submit(machines_q, data_to_float)
    return machines_q

machines = {
    'var': 'CRT.Machines',
    'create_question': create_machines_q,
    'answer': {
        'correct': 5,
        'intuitive': 100
    }
}

LILY_PADS_TXT = """
<p>In a lake, there is a patch of lily pads. Every day, the patch doubles in size.</p>
<p>If it takes 48 days for the patch to covert the entire lake, how many days would it take for the patch to covert half of the lake?</p>
"""

def create_lily_pads_q():
    lily_pads_q = Free(text=LILY_PADS_TXT, append='days')
    Validate(lily_pads_q, require)
    Validate(lily_pads_q, numeric)
    Submit(lily_pads_q, data_to_float)
    return lily_pads_q

lily_pads = {
    'var': 'CRT.LilyPads',
    'create_question': create_lily_pads_q,
    'answer': {
        'correct': 47,
        'intuitive': 24
    }
}