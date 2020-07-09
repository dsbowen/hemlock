"""Hello World: a starting example"""

# UG:
    # comprehension check
    # Assigner
# debugging
# deployment

from hemlock import Branch, Check, Compile, Embedded, Input, Label, Navigate, Page, Range, Select, Submit, Validate, route
from hemlock.tools import comprehension_check, join

from datetime import datetime
from random import randint

POT = 20

# @route('/survey')
def start():
    demographics_page = Page(
        Submit.record_age(Validate.validate_date_format(Input(
            '<p>Enter your date of birth.</p>',
            placeholder='mm/dd/yyyy',
            var='DoB', data_rows=-1
        ))),
        Validate.require(Check(
            '<p>Indicate your gender.</p>',
            ['Male', 'Female', 'Other'],
            var='Gender', data_rows=-1
        )),
        Validate.require(Check(
            '<p>Indicate your race or ethnicity. Check as many as apply.</p>',
            [
                'White',
                'Black or African-American',
                'Asian',
                'Native Hawaiian or other Pacific Islander',
                'Other',
            ],
            multiple=True,
            var='Race', data_rows=-1
        )),
        Select(
            '<p>Select your current marital status.</p>',
            [
                'Married',
                'Widowed',
                'Divorced',
                'Separated',
                'Never married',
            ],
            var='MaritalStatus', data_rows=-1
        ),
        Range(
            '''
            <p>Indicate your 'subjective socio-economic status'.</p>
            
            <p>At the right end of the scale are the people who are the 
            best off; those who have the most money, the most 
            education, and the best jobs. On the left are the people 
            who are the worst off; those who have the least money, the 
            least education, and the worst jobs (or are unemployed). 
            Please indicate where you think you stand on this scale.</p>
            ''',
            min=0, max=10,
            var='SubjectiveSES', data_rows=-1
        )
    )
    return Navigate.ultimatum_game(Branch(
        demographics_page,
        Page(Compile.confirm(Label(), demographics_page), back=True)
    ))

@Validate.register
def validate_date_format(inpt):
    try:
        # try to convert to a datetime object
        datetime.strptime(inpt.response, '%m/%d/%Y')
    except:
        # if this fails, the participant entered an invalid response
        return '<p>Format your date of birth as mm/dd/yyyy.</p>'

@Submit.register
def record_age(inpt):
    # calculate age in years
    date_of_birth = datetime.strptime(inpt.data, '%m/%d/%Y')
    age = (datetime.utcnow() - date_of_birth).days / 365.25
    # record age as embedded data
    inpt.page.embedded = [Embedded('Age', age, data_rows=-1)]

@Compile.register
def confirm(label, demographics_page):
    demographics = [q.data for q in demographics_page.questions]
    race = demographics_page.questions[2]
    race = join('and', *(key for key in race.data if race.data[key]))
    demographics[2] = race
    label.label = '''
    <p>Confirm the following information:</p>
    <ul>
        <li>Date of birth: {}</li>
        <li>Gender: {}</li>
        <li>Race/Ethnicity: {}</li>
        <li>Marital status: {}</li>
        <li>Subjective socio-economic status: {}</li>
    </ul>
    <p>To correct this information, click '<<'.</p>
    '''.format(*demographics)

# @Navigate.register
@route('/survey')
def ultimatum_game(start_branch=None):
    branch = comprehension_check(
        Branch(),
        Page(Label('''
        <p>You are about to play an ultimatum game. The game involves two
        players: a <b>proposer</b> and a <b>responder</b>. The proposer has 
        ${} to split between him/herself and the responder. The responder 
        names an amount of money such that he/she accepts any proposed 
        split which gives him/her at least this amount, and rejects any 
        proposed split which gives him/her less than this amount.</p>

        <p>If the split is accepted, the proposer and responder split the 
        money according to the proposal. If the split is rejected, both 
        players receive $0.</p>

        <p>We will test your understanding of these instructions on the 
        next page.</p>
        '''.format(POT))),
        [gen_check_page(accept=True), gen_check_page(accept=False)]
    )
    branch.pages.append(Page(
        Label('<p>You passed the check!</p>'), terminal=True)
    )
    return branch

def gen_check_page(accept):
    return Compile.clear_response(Compile.random_proposal(
        Page(
            Label(),
            Input(
                '<p>How much money does the proposer receive?</p>',
                prepend='$',
                append='.00'
            ),
            Input(
                '<p>How much money does the responder receive?</p>',
                prepend='$',
                append='.00'
            )
        ),
        accept=accept
    ))

@Compile.register
def random_proposal(page, accept):
    # randomly generate a proposed split and response
    n = randint(1, POT-1)
    proposal = n, POT-n
    response = randint(0, POT-n-1) if accept else randint(POT-n, POT)
    # compute the payoff
    payoff = proposal if response<=proposal[1] else (0, 0)
    # describe the proposal and response in the label
    page.questions[0].label = '''
    <p>Imagine the proposer proposes the following split:</p>
    <ul>
       <li>Proposer: ${}</li>
       <li>Responder: ${}</li>
    </ul>
    <p>The responder says, "I will accept any proposal which gives 
    me at least ${}."</p>
    '''.format(*proposal, response)
    # add submit functions to verify that the response was correct
    page.questions[1].submit_functions.clear()
    Submit.match(page.questions[1], str(payoff[0]))
    page.questions[2].submit_functions.clear()
    Submit.match(page.questions[2], str(payoff[1]))