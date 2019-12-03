"""Cognitive Reflection Test"""

from hemlock_crt.items import *

from hemlock import *
from random import shuffle

def CRT(*items):
    crt_b = Branch()
    [create_page(crt_b, i) for i in items]
    shuffle(crt_b.pages)
    Submit(crt_b.pages[-1], summary_stats, args=[crt_b])
    return crt_b

def create_page(crt_b, item):
    p = Page(crt_b)
    var = item.get('var')
    p.timer.var = '{}Time'.format(var)
    p.timer.all_rows = True
    q = Free(
        p,
        text=item.get('text'),
        append=item.get('units'),
        var=var,
        all_rows=True
    )
    [Validate(q, func) for func in item.get('validate', [])]
    correct_q = Embedded(
        page=p, 
        var='{}Correct'.format(var), 
        all_rows=True
    )
    intuitive_q = Embedded(
        page=p, 
        var='{}Intuitive'.format(var),
        all_rows=True
    )
    Submit(p, assess_response, kwargs=item.get('answer', {}))

def assess_response(p, correct=None, intuitive=None):
    crt_q, correct_q, intuitive_q = p.questions
    correct_q.data = int(crt_q.response == correct)
    intuitive_q.data = int(crt_q.response == intuitive)

def summary_stats(last_p, crt_b):
    correct = sum([p.questions[1].data for p in crt_b.pages])
    intuitive = sum([p.questions[2].data for p in crt_b.pages])
    sum_stats = [
        (correct, 'CRT.TotalCorrect'),
        (100.0 * correct / len(crt_b.pages), 'CRT.PctCorrect'),
        (intuitive, 'CRT.TotalIntuitive'),
        (100.0 * intuitive / len(crt_b.pages), 'CRT.PctIntuitive')
    ]
    [Embedded(branch=crt_b, data=data, var=var) for data, var in sum_stats]
