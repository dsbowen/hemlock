"""Hemlock survey"""

from hemlock import *
from texts import *

# CRT if answer is None
# interval checks for valid conversion using try except

from hemlock_crt import CRT, ball_bat, machines, lily_pads

from hemlock_nash import GameMixin, PlayerMixin, StrategyMixin, PayoffMixin
from hemlock_nash.IPD import description, payoff_function, tit_for_tat
from random import random

ROUNDS = 10
P_NOISE = .1
PAYOFF_MATRIX = {
    ('Cooperate','Cooperate'): (3,3),
    ('Cooperate','Defect'): (0,5),
    ('Defect','Cooperate'): (5,0),
    ('Defect','Defect'): (1,1)
}

def noisy_tft(player):
    action = tit_for_tat(player, first_action='Cooperate')
    if random() < P_NOISE:
        action = 'Cooperate' if action == 'Defect' else 'Defect'
    return action

class Game(GameMixin, db.Model):
    pass

class Player(PlayerMixin, db.Model):
    pass

class Strategy(StrategyMixin, db.Model):
    pass

class Payoff(PayoffMixin, db.Model):
    pass

def Start(root=None):
    b = CRT(ball_bat, machines, lily_pads)
    Navigate(b, IPD)
    return b
    
def IPD(root=None):
    g = Game()
    Player(g, name='Red', strategy=noisy_tft)
    Player(g, name='Blue', strategy=noisy_tft)
    Payoff(g, payoff_function, args=[PAYOFF_MATRIX])
    g.play()

    b = Branch()
    p = Page(b)
    Text(p, text=description(PAYOFF_MATRIX))
    for i in range(ROUNDS):
        p = Page(b, cache_compile=True)
        Compile(p, update_game, args=[g])
        Submit(p, record_accuracy, args=[g])
    p = Page(b, terminal=True)
    Text(p, text='<p>Thank you for participating.</p>')
    return b

def update_game(page, game):
    Text(page, text=game.html_table())
    est_q = Free(
        page,
        text='<p>How likely do you think Red is to Cooperate in the next round?</p>',
        append='%',
        var='RedCoopEst'
    )
    Validate(est_q, require)
    Validate(est_q, numeric)
    Validate(est_q, interval, args=[0.0,100.0])

def record_accuracy(page, game):
    est_q = page.questions[-1]
    est_q.data = float(est_q.data) / 100
    game.play()
    red_coop = int(game.actions['Red'][-1] == 'Cooperate')
    blue_coop = int(game.actions['Blue'][-1] == 'Cooperate')
    Embedded(page, data=red_coop, var='RedCoop')
    Embedded(page, data=blue_coop, var='BlueCoop')
    Embedded(page, data=(est_q.data - red_coop)**2, var='Brier')