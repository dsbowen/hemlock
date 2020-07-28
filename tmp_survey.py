from hemlock import Branch, Check, Compile as C, Debug as D, Embedded, Input, Label, Navigate as N, Page, Range, Select, Submit as S, Validate as V, route
from hemlock.tools import Assigner, comprehension_check, join

import random
from datetime import datetime
from random import randint

# the number of rounds participants play
N_ROUNDS = 5
# the amount of money split
POT = 20

assigner = Assigner({'Proposer': (0, 1)})

@route('/survey')
def start():
    demographics_page = Page(
        Input(
            '<p>Enter your date of birth.</p>',
            placeholder='mm/dd/yyyy',
            var='DoB', data_rows=-1,
            validate=[V.require(), V.date_format()],
            submit=S.record_age(),
            debug=[D.send_keys(), D.send_keys('10/26/1992', p_exec=.8)]
        ),
        Check(
            '<p>Indicate your gender.</p>',
            ['Male', 'Female', 'Other'],
            var='Gender', data_rows=-1,
            validate=V.require()
        ),
        Check(
            '<p>Indicate your race or ethnicity. Check as many as apply.</p>',
            [
                'White',
                'Black or African-American',
                'Asian',
                'Native Hawaiian or other Pacific Islander',
                'Other',
            ],
            multiple=True, var='Race', data_rows=-1,
            validate=V.require()
        ),
        Select(
            '<p>Select your current marital status.</p>',
            [
                'Married',
                'Widowed',
                'Divorced',
                'Separated',
                'Never married',
            ],
            var='MaritalStatus', data_rows=-1,
        ),
        Range(
            '''
            <p>At the right end of the scale are the people who are the 
            best off; those who have the most money, the most 
            education, and the best jobs. On the left are the people 
            who are the worst off; those who have the least money, the 
            least education, and the worst jobs (or are unemployed). 
            Please indicate where you think you stand on this scale.</p>
            ''',
            min=0, max=10, var='SubjectiveSES', data_rows=-1,
        ),
    )
    return Branch(
        demographics_page,
        Page(
            Label(compile=C.confirm(demographics_page)),
            back=True
        ),
        navigate=N.ultimatum_game()
    )

@V.register
def date_format(inpt):
    try:
        # try to convert to a datetime object
        datetime.strptime(inpt.response, '%m/%d/%Y')
    except:
        # if this fails, the participant entered an invalid response
        return '<p>Format your date of birth as mm/dd/yyyy.</p>'

@S.register
def record_age(inpt):
    # calculate age in years
    date_of_birth = datetime.strptime(inpt.data, '%m/%d/%Y')
    age = (datetime.utcnow() - date_of_birth).days / 365.25
    # record age as embedded data
    inpt.page.embedded = [Embedded('Age', age, data_rows=-1)]

@C.register
def confirm(confirm_label, demographics_page):
    # get the participant's data from the demographics page
    demographics = [q.data for q in demographics_page.questions]
    # re-format the race demographic data
    race = demographics_page.questions[2]
    race = join('and', *(key for key in race.data if race.data[key]))
    demographics[2] = race
    # set the label based on the participant's demographics data
    confirm_label.label = '''
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

@N.register
def ultimatum_game(start_branch):
    proposer = assigner.next()['Proposer']
    return Branch(
        *comprehension_check(
            instructions=Page(
                Label(
                    '''
                    <p>You are about to play an ultimatum game. The game 
                    involves two players: a <b>proposer</b> and a 
                    <b>responder</b>. The proposer has ${} to split between 
                    him/herself and the responder. The responder names an 
                    amount of money such that he/she accepts any proposed 
                    split which gives him/her at least this amount, and 
                    rejects any proposed split which gives him/her less 
                    than this amount.</p>

                    <p><b>If the split is accepted, the proposer and 
                    responder split the money according to the proposal. If 
                    the split is rejected, both players receive $0.</b></p>

                    <p>You will play {} rounds of this game. Each round you 
                    will be paired with another randomly selected 
                    participant. <b>You will rarely, if ever, play two 
                    rounds with the same player.</b>

                    <p>We will test your understanding of the instructions 
                    on the next page.</p>
                    '''.format(POT, N_ROUNDS)
                )
            ),
            checks=[gen_check_page(accept=True), gen_check_page(accept=False)]
        ),
        Page(
            Label(
                '''
                <p>You are about to play an ultimatum game as a <b>{}</b>.</p>
                '''.format('proposer' if proposer else 'responder')
            )
        ),
        navigate=N.proposer_branch() if proposer else N.responder_branch()
    )

def gen_check_page(accept):
    return Page(
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
        ),
        compile=[C.clear_response(), C.random_proposal(accept)]
    )

@C.register
def random_proposal(check_page, accept):
    # randomly generate a proposed split and response
    n = randint(1, POT-1)
    proposal = POT-n, n # proposer receives POT-n, responder receives n
    response = randint(0, n) if accept else randint(n+1, POT)
    # compute the payoff
    payoff = proposal if response<=proposal[1] else (0, 0)
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
    check_page.questions[1].submit = S.match(str(payoff[0]))
    check_page.questions[2].submit = S.match(str(payoff[1]))
    check_page.questions[1].debug = [
        D.send_keys(), D.send_keys(str(payoff[0]), p_exec=.8)
    ]
    check_page.questions[2].debug = [
        D.send_keys(), D.send_keys(str(payoff[1]), p_exec=.8)
    ]

@N.register
def proposer_branch(ultimatum_game_branch):
    branch = Branch()
    for round_ in range(N_ROUNDS):
        proposal_input = gen_proposal_input(round_+1)
        branch.pages.append(Page(proposal_input))
        branch.pages.append(Page(
            Label(compile=C.proposer_outcome(proposal_input)),
            cache_compile=True
        ))
    branch.pages.append(Page(
        Label('<p>Thank you for completing the hemlock tutorial!</p>'),
        terminal=True      
    ))
    return branch

def gen_proposal_input(round_):
    return Input(
        '''
        <p><b>Round {} of {}</b></p>
        <p>You have ${} to split between you and the responder. How 
        much money would you like to offer to the responder?</p>
        '''.format(round_, N_ROUNDS, POT),
        prepend='$', append='.00', var='Proposal',
        validate=V.range_val(0, POT),
        submit=S.data_type(int),
        debug=[D.send_keys(), D.send_keys(str(randint(0, POT)), p_exec=.8)]
    )

@C.register
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

@N.register
def responder_branch(ultimatum_game_branch=None):
    branch = Branch()
    for round_ in range(N_ROUNDS):
        response_input = gen_response_input(round_+1)
        branch.pages.append(Page(response_input))
        branch.pages.append(Page(
            Label(compile=C.responder_outcome(response_input)),
            cache_compile=True
        ))
    branch.pages.append(Page(
        Label('<p>Thank you for completing the hemlock tutorial!</p>'),
        terminal=True        
    ))
    return branch

def gen_response_input(round_):
    return Input(
        '''
        <p><b>Round {} of {}</b></p>
        <p>The proposer has ${} to split between him/herself and you. Complete
        this sentence:</p>
        <p>I will accept any proposal which gives me at least</p>
        '''.format(round_, N_ROUNDS, POT),
        prepend='$', append='.00', var='Response',
        validate=V.range_val(0, POT),
        submit=S.data_type(int),
        debug=[D.send_keys(), D.send_keys(str(randint(0, POT)), p_exec=.8)]
    )

@C.register
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