"""Hemlock survey"""

from random import random

from hemlock import *
from hemlock.app import db
from texts import *

from flask_login import current_user
from hemlock_crt import CRT, ball_bat, machines, lily_pads
from hemlock_nash import GameMixin, PlayerMixin, StrategyMixin, PayoffMixin
from hemlock_nash.IPD import description, payoff_function, tit_for_tat
from sqlalchemy.orm import backref

P_NOISE = .1
PAYOFF_MATRIX = {
    ('Cooperate','Cooperate'): (3,3),
    ('Cooperate','Defect'): (0,5),
    ('Defect','Cooperate'): (5,0),
    ('Defect','Defect'): (1,1)
}
ROUNDS = 2


class Game(GameMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    part = db.relationship(
        'Participant', 
        backref=backref('game', uselist=False)
    )


class Player(PlayerMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Strategy(StrategyMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Payoff(PayoffMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)


def noisy_tft(player):
    action = tit_for_tat(player, first_action='Cooperate')
    if random() < P_NOISE:
        return 'Cooperate' if action == 'Defect' else 'Defect'
    return action

def Start(root=None):
    crt_branch = CRT(ball_bat)
    Navigate(crt_branch, IPD)
    return crt_branch

def IPD(root=None):
    g = Game(description=description(PAYOFF_MATRIX))
    g.part = current_user
    Player(g, name='Red', strategy=noisy_tft)
    Player(g, name='Blue', strategy=noisy_tft)
    Payoff(g, payoff_function, args=[PAYOFF_MATRIX])

    b = Branch()
    p = Page(b)
    Text(p, text=g.description)
    [create_prediction_page(b) for i in range(ROUNDS)]
    p = Page(b, terminal=True)
    Text(p, text='<p>Thank you for your participation.<p>')
    return b

def create_prediction_page(b):
    p = Page(b, cache_compile=True)
    CompileWorker(p)
    Text(p, text='<p>Below is a summary of the game so far.</p>')
    game_history_txt = Text(p)
    Compile(game_history_txt, play_game, args=[current_user.game])
    red_q = Free(p, text='<p>How likely do you think the Red player is to Cooperate in the next round?</p>', append='%', var='RedCooperatedHat')
    Validate(red_q, require)
    Validate(red_q, numeric)
    Submit(p, record_gameplay)

def play_game(game_history_txt, game):
    game.play()
    game_history_txt.text = game.html_table()

def record_gameplay(page):
    red_q = page.questions[-1]
    red_q.data = float(red_q.data) / 100.0
    red_action = current_user.game.players[0].actions[-1]
    red_action = int(red_action == 'Cooperate')
    Embedded(page=page, data=red_action, var='RedCooperated')
    Embedded(page=page, data=(red_q.data - red_action)**2, var='Brier')