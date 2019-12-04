"""Cognitive Reflection Test"""

from hemlock import *

def CRT(*items):
    crt_b = Branch()
    [create_page(crt_b, i) for i in items]
    Submit(crt_b.pages[-1], summary_stats, args=[crt_b])
    return crt_b

def create_page(crt_b, item):
    p = Page(crt_b)
    var = item.get('var')
    p.timer.var = '{}Time'.format(var)
    p.timer.all_rows = True
    q = item['create_question']()
    q.page, q.var, q.all_rows = p, var, True
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
    Submit(p, assess_response, kwargs=item['answer'])

def assess_response(p, correct, intuitive):
    crt_q, correct_q, intuitive_q = p.questions
    correct_q.data = int(crt_q.data == correct)
    intuitive_q.data = int(crt_q.data == intuitive)

def summary_stats(last_p, crt_b):
    correct = sum([p.questions[1].data for p in crt_b.pages])
    intuitive = sum([p.questions[2].data for p in crt_b.pages])
    sum_stats = [
        (correct, 'CRT.TotalCorrect'),
        (100.0 * correct / len(crt_b.pages), 'CRT.PctCorrect'),
        (intuitive, 'CRT.TotalIntuitive'),
        (100.0 * intuitive / len(crt_b.pages), 'CRT.PctIntuitive')
    ]
    [
        Embedded(branch=crt_b, data=data, var=var, all_rows=True) 
        for data, var in sum_stats
    ]
