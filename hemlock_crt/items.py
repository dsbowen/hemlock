from hemlock import require, numeric

BALL_BAT_TXT = """
<p>A bat and ball cost $1.10 in total. The bat costs $1.00 more than the ball.</p>
<p>How much does the ball cost?</p>
"""

ball_bat = {
    'var': 'CRT.BallBat',
    'text': BALL_BAT_TXT,
    'units': 'cents',
    'validate': [
        require,
        numeric
    ],
    'answer': {
        'correct': '5',
        'intuitive': '10'
    }
}

MACHINES_TXT = """
<p>If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?
"""

machines = {
    'var': 'CRT.Machines',
    'text': MACHINES_TXT,
    'units': 'minutes',
    'validate': [
        require,
        numeric
    ],
    'answer': {
        'correct': '5',
        'intuitive': '100'
    }
}

LILY_PADS_TXT = """
<p>In a lake, there is a patch of lily pads. Every day, the patch doubles in size.</p>
<p>If it takes 48 days for the patch to covert the entire lake, how long would it take for the patch to covert half of the lake?</p>
"""

lily_pads = {
    'var': 'CRT.LilyPads',
    'text': LILY_PADS_TXT,
    'units': 'days',
    'validate': [
        require,
        numeric
    ],
    'answer': {
        'correct': '47',
        'intuitive': '24'
    }
}