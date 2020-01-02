"""Data storage"""

import compile_functions

from hemlock import *

from random import shuffle

@Navigate.register
def DataStorage(origin=None):
    b = Branch()
    Navigate.CompileFunctions(b)

    """Variable setting"""
    p = Page(b)
    Input(
        p, 
        label="<p>Set a question's variable to store its data.</p>", 
        var='TestVar'
    )

    """Date and time inputs"""
    p = Page(b)
    Label(
        p,
        label='<p>Date and time input data are converted to `datetime` objects on submission.</p>'
    )
    Input(
        p, 
        label='<p>This is a `date` input.</p>',
        input_type='date',
        var='Date'
    )
    Input(
        p, 
        label='<p>This is a `datetime-local` input.</p>',
        input_type='datetime-local',
        var='Datetime'
    )
    Input(
        p, 
        label='<p>This is a `month` input.</p>',
        input_type='month',
        var='Month'
    )
    Input(
        p, 
        label='<p>This is a `time` input.</p>',
        input_type='time',
        var='Time'
    )
    Input(
        p, 
        label='<p>This is a `week` input.</p>',
        input_type='week',
        var='Week'
    )

    """Choice questions"""
    p = Page(b)
    c = Check(
        p,
        label='<p>Values for choice questions can be set in the `Choice` object.<p>',
        var='ChoiceVar'
    )
    Choice(c, label='Yes', value=1)
    Choice(c, label='No', value=0)

    s = Select(
        p,
        label='<p>Data from mulple choice questions are automatically one-hot encoded.</p>',
        multiple=True,
        var='MultiChoiceVar'
    )
    Option(s, label='Red', value='R')
    Option(s, label='Green', value='G')
    Option(s, label='Blue', value='B')

    """Variable order"""
    p = Page(b)
    Label(
        p, 
        label="""
        <p>Question data are stored in the order in which the questions are <i>created</i>.</p>
        <p>On the next page, enter the names of four of your friends.</p>
        <p>Although the inputs are randomized, they will be properly ordered when you download the data.</p>
        """
    )

    p = Page(b)
    for i in range(4):
        Input(
            p, 
            label='<p>Enter the name of friend {}.</p>'.format(i+1), 
            var='Friends'
        )
    shuffle(p.questions)

    """Allrows"""
    p = Page(b)
    Input(
        p,
        label="""
        <p>You can set the data from a question to appear in all rows associated with a participant.</p>
        <p>Enter your name.</p>
        """,
        var='Name',
        all_rows=True
    )

    """Timer"""
    p = Page(b)
    p.timer.var = 'TimerVar'
    p.timer.all_rows = True
    Label(
        p,
        label="""
        <p>All `Page`s have a `Timer`.</p>
        <p>Expose the timer's data by settings its variable.</p>
        """
    )

    """Embedded data"""
    p = Page(b)
    Label(
        p,
        label='<p>You can store other data using the `embedded` data associated with `Page`s and `Branch`es.</p>'
    )
    Embedded(p, data='This is embedded data', var='EmbeddedVar')

    return b