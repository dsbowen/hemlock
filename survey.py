"""Hemlock tutorial"""

# https://devcenter.heroku.com/articles/setting-up-apps-using-the-heroku-platform-api
# make app.json
# hlk deploy runs app setup using the platform API and configures the bucket
# 1) commit to git
# 2) run app setup using tarball
# 3) configure bucket

from hemlock import Branch, Check, Compile, Debug, Embedded, Input, Label, Navigate, Page, Range, Select, Submit, Validate, route, settings
from hemlock.tools import Assigner, comprehension_check, join

import random
from datetime import datetime
from random import randint

N_ROUNDS = 5
POT = 20

settings.update({'password': 'my-password'})
assigner = Assigner({'Proposer': (0,1)})

@route('/survey')
def start():
    demographics_page = Page(
        Debug.send_keys(
            Submit.record_age(Validate.validate_date_format(Input(
                '<p>Enter your date of birth.</p>',
                placeholder='mm/dd/yyyy',
                var='DoB', data_rows=-1
            ))),
            '10/26/1992', p_exec=.8
        ),
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

@Navigate.register
def ultimatum_game(start_branch):
    branch = comprehension_check(
        Branch(),
        Page(Label('''
        <p>You are about to play an ultimatum game. The game involves two
        players: a <b>proposer</b> and a <b>responder</b>. The proposer has 
        ${} to split between him/herself and the responder. The responder 
        names an amount of money such that he/she accepts any proposed 
        split which gives him/her at least this amount, and rejects any 
        proposed split which gives him/her less than this amount.</p>

        <p><b>If the split is accepted, the proposer and responder split the 
        money according to the proposal. If the split is rejected, both 
        players receive $0.</b></p>

        <p>You will play {} rounds of this game. Each round, you will be 
        paired with another randomly selected participant. <b>You will rarely,
        if ever, play two rounds with the same player.</b>

        <p>We will test your understanding of these instructions on the 
        next page.</p>
        '''.format(POT, N_ROUNDS))),
        [gen_check_page(accept=True), gen_check_page(accept=False)]
    )
    proposer = assigner.next()['Proposer']
    branch.pages.append(Page(
        Label('''
            <p>You are about to play an ultimatum game as a <b>{}</b>.</p>
        '''.format('proposer' if proposer else 'responder')
        ),
    ))
    if proposer:
        return Navigate.proposer_branch(branch)
    else:
        return Navigate.responder_branch(branch)

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
def random_proposal(check_page, accept):
    # randomly generate a proposed split and response
    n = randint(1, POT-1)
    proposal = POT-n, n # proposer receives POT-n, responder receives n
    response = randint(0, n) if accept else randint(n+1, POT)
    # compute the payoff
    payoff = proposal if response <= proposal[1] else (0, 0)
    # describe the proposal and response in the label
    check_page.questions[0].label = '''
    <p>Imagine the proposer proposes the following split:</p>
    <ul>
       <li>Proposer: ${}</li>
       <li>Responder: ${}</li>
    </ul>
    <p>The responder says, "I will accept any proposal which gives 
    me at least ${}."</p>
    '''.format(*proposal, response)
    # add submit functions to verify that the response was correct
    check_page.questions[1].submit_functions.clear()
    Debug.send_keys(
        Submit.match(check_page.questions[1], str(payoff[0])), 
        str(payoff[0]), p_exec=.8
    )
    check_page.questions[2].submit_functions.clear()
    Debug.send_keys(
        Submit.match(check_page.questions[2], str(payoff[1])),
        str(payoff[1]), p_exec=.8
    )

@Navigate.register
def proposer_branch(ultimatum_game_branch=None):
    branch = Branch()
    for round_ in range(N_ROUNDS):
        proposal_input = gen_proposal_input(round_+1)
        branch.pages.append(Page(proposal_input))
        branch.pages.append(Page(Compile.proposer_outcome(
            Label(), proposal_input
        )))
    branch.pages.append(Page(
        Label('<p>Thank you for completing the hemlock tutorial!</p>'),
        terminal=True      
    ))
    return branch

def gen_proposal_input(round_):
    return Debug.send_keys(
        Submit.data_type(
            Validate.range_val(
                Input(
                    '''
                    <p><b>Round {} of {}</b></p>
                    <p>You have ${} to split between you and the responder. 
                    How much money would you like to offer to the responder?
                    </p>
                    '''.format(round_, N_ROUNDS, POT),
                    prepend='$',
                    append='.00',
                    var='Proposal'
                ),
                min_=0, max_=POT
            ),
            int
        ),
        str(randint(0, POT)), p_exec=.8
    )

@Compile.register
def proposer_outcome(outcome_label, proposal_input):
    # get the proposal
    proposal = POT-proposal_input.data, proposal_input.data
    # get all responses
    response_inputs = Input.query.filter(
        Input.var=='Response', Input.data!=None
    ).all()
    if response_inputs:
        # randomly choose a response
        response = random.choice(response_inputs).data
    else:
        # no responses are available
        # e.g. if this is the first participant
        response = randint(0, POT)
    # compute the payoff
    accept = response <= proposal[1]
    payoff = proposal if accept else (0, 0)
    # record results as embedded data
    outcome_label.page.embedded = [
        Embedded('Response', response),
        Embedded('Accept', int(accept)),
        Embedded('ProposerPayoff', payoff[0]),
        Embedded('ResponderPayoff', payoff[1])
    ]
    # describe the outcome of the round
    outcome_label.label = '''
        <p>You proposed the following split:</p>
        <ul>
            <li>You: ${}</li>
            <li>Responder: ${}</li>
        </ul>
        <p>The responder said they will accept any proposal which gives
        them at least ${}.</p>
        <p><b>Your proposal was {}, giving you a payoff of ${}.</b></p>
    '''.format(
        *proposal, response, 'accepted' if accept else 'rejected', payoff[0]
    )

@Navigate.register
def responder_branch(ultimatum_game_branch=None):
    branch = Branch()
    for round_ in range(N_ROUNDS):
        response_input = gen_response_input(round_+1)
        branch.pages.append(Page(response_input))
        branch.pages.append(Page(Compile.responder_outcome(
            Label(), response_input
        )))
    branch.pages.append(Page(
        Label('<p>Thank you for completing the hemlock tutorial!</p>'),
        terminal=True        
    ))
    return branch

def gen_response_input(round_):
    return Debug.send_keys(
        Submit.data_type(
            Validate.range_val(
                Input(
                    '''
                    <p><b>Round {} of {}</b></p>
                    <p>The proposer has ${} to split between him/herself and 
                    you. Complete this sentence:</p>
                    <p>I will accept any proposal which gives me at least</p>
                    '''.format(round_, N_ROUNDS, POT),
                    prepend='$',
                    append='.00',
                    var='Response'
                ),
                min_=0, max_=POT
            ),
            int
        ),
        str(randint(0, POT)), p_exec=.8
    )

@Compile.register
def responder_outcome(outcome_label, responder_input):
    # get the response
    response = responder_input.data
    # randomly select a proposal
    proposal_inputs = Input.query.filter(
        Input.var=='Proposal', Input.data!=None
    ).all()
    if proposal_inputs:
        # randomly choose a proposal
        n = random.choice(proposal_inputs).data
    else:
        # no proposals are available
        # e.g. if this is the first participant
        n = randint(0, POT)
    proposal = POT-n, n
    # compute the payoff
    accept = response <= proposal[1]
    payoff = proposal if accept else (0, 0)
    # record results as embedded data
    outcome_label.page.embedded = [
        Embedded('Proposal', proposal[1]),
        Embedded('Accept', int(accept)),
        Embedded('ProposerPayoff', payoff[0]),
        Embedded('ResponderPayoff', payoff[1])
    ]
    # describe the outcome of the round
    outcome_label.label = '''
        <p>The proposer proposed the following split:</p>
        <ul>
            <li>Proposer: ${}</li>
            <li>You: ${}</li>
        </ul>
        <p>You said you will accept any proposal which gives you at 
        least ${}.</p>
        <p><b>You {} the proposal, giving you a payoff of ${}.</b></p>
    '''.format(
        *proposal, response, 'accepted' if accept else 'rejected', payoff[1]
    )