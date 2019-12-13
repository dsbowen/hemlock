"""Hemlock survey"""

from hemlock import *
from texts import *

from hemlock_crt import CRT, ball_bat, machines, lily_pads

from hemlock_nash import GameMixin, PlayerMixin, StrategyMixin, PayoffMixin
from hemlock_nash.IPD import payoff_function, tit_for_tat

PAYOFF_MATRIX = {
    ('c','c'): (3,3),
    ('c','d'): (0,5),
    ('d','c'): (5,0),
    ('d','d'): (1,1)
}

class Game(GameMixin, db.Model):
    pass

class Player(PlayerMixin, db.Model):
    pass

class Strategy(StrategyMixin, db.Model):
    pass

class Payoff(PayoffMixin, db.Model):
    pass

def noisy_tft(player):
    return tit_for_tat(player, first_action='c')

def Start(root=None):
    b = CRT(ball_bat, machines, lily_pads)
    Navigate(b, IPD)
    return b

def IPD(root=None):
    g = Game()
    Player(g, name='Red', strategy=noisy_tft)
    Player(g, name='Blue', strategy=noisy_tft)
    Payoff(g, payoff_function, args=[PAYOFF_MATRIX])

    b = Branch()
    for i in range(10):
        g.play()
        p = Page(b)
        Text(p, text=g.html_table())
        Free(p, var='est')
    p = Page(b, terminal=True)
    Text(p, text='Hello World')
    return b