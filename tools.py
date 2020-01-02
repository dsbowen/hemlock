"""Tools"""

import workers

from hemlock import *

@Navigate.register
def Tools(origin=None):
    b = Branch()
    Navigate.ComprehensionCheck(b)

    """Even randomize"""
    elements = ['Red','Green','Blue']
    colors = even_randomize(tag='colors', elements=elements, r=2)
    p = Page(b)
    Label(
        p,
        label="""
        <p>`even_randomize` randomizes over all permutations or combinations of the given elements.</p>
        <p>It presents these evenly across participants.</p>
        <p>Your chosen colors are {0} and {1}.</p>
        """.format(*colors)
    )

    """Random assign"""
    p = Page(b)
    conditions = {
        'Condition1': (0,1),
        'Condition2': ('low','med','high')
    }
    assignment = random_assign(b, tag='conditions', conditions=conditions)
    Label(
        p,
        label="""
        <p>You were randomly assigned to Condition 1: {0} and Condition 2: {1}.</p>
        <p>Assignments are recorded as embedded data on the `parent` object (in this case, the branch).</p>
        """.format(assignment['Condition1'], assignment['Condition2'])
    )

    """Custom javascript (custom css is similar)"""
    p = Page(b)
    src = url_for('static', filename='custom_js.js')
    custom_js = gen_external_js(src=src)
    p.js.append(custom_js)
    p.js.changed()
    Label(p, label='<p>Lorem ipsum.<p>')

    """Images"""
    p = Page(b)
    img = Img(
        caption='Wanna See the Code?',
        alignment='center',
        src='https://imgs.xkcd.com/comics/wanna_see_the_code.png'
    )
    Label(p, label=img.render())

    """Images as choices"""
    p = Page(b)
    c = Check(p, label='<p>Which cartoon do you like best?</p>')
    img = Img(src='https://imgs.xkcd.com/comics/halting_problem.png')
    Choice(c, label=img.render())
    img = Img(src='https://imgs.xkcd.com/comics/xkcde.png')
    Choice(c, label=img.render())
    img = Img(src='https://imgs.xkcd.com/comics/code_quality_2.png')
    Choice(c, label=img.render())

    """Videos"""
    p = Page(b)
    vid = Vid.from_youtube('https://www.youtube.com/watch?v=fJ9rUzIMcZQ')
    vid.parms['autoplay'] = 1
    Label(p, label=vid.render())

    return b

@Navigate.register
def ComprehensionCheck(origin=None):
    instructions, checks = [], []

    p = Page()
    Label(
        p, 
        label="""
        <p>A comprehension check consists of 'instruction' pages followed by 'check' pages.</p>
        <p>The data in all questions of a check page must evaluate to `True` to pass the check.</p>
        <p>When you fail a check, you are brought back to the first instructions page.</p>
        <p>However, once you reread the instructions, you do not have to repeat any checks you already passed.</p>
        """
    )
    instructions.append(p)

    p = Page()
    Label(p, label='<p>Instructions page 2.</p>')
    instructions.append(p)

    p = Page()
    s = Select(p, label='<p>Select the correct answer.</p>')
    Option(s, label='Incorrect', value=0)
    Option(s, label='Correct', value=1)
    Debug.click_choices(s, s.choices[-1], p_exec=.9)
    checks.append(p)

    p = Page()
    i = Input(p, label='<p>Enter "the correct answer".</p>')
    Submit.match(i, 'the correct answer')
    Debug.send_keys(i, 'the correct answer', p_exec=.9)
    checks.append(p)

    b = comprehension_check(instructions=instructions, checks=checks, attempts=2)
    Navigate.Workers(b)
    return b