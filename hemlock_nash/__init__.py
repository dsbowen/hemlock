"""Hemlock extension for games"""

from hemlock.database import Base
from hemlock.database.types import MarkupType
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship
from sqlalchemy_function import FunctionMixin
from sqlalchemy_mutable import MutableListType
from sqlalchemy_orderingitem import OrderingItem


class GameMixin(Base):
    description = Column(MarkupType)
    rounds = Column(Integer, default=0)

    @declared_attr
    def players(cls):
        return relationship(
            'Player',
            backref='game',
            order_by='Player.index',
            collection_class=ordering_list('index')
        )
    
    @declared_attr
    def payoff_function(cls):
        return relationship(
            'Payoff',
            backref='game',
            uselist=False
        )
    
    @property
    def actions(self):
        return {p.name: p.actions for p in self.players}

    @property
    def payoffs(self):
        return {p.name: p.payoffs for p in self.players}

    @property
    def cum_payoffs(self):
        return {p.name: p.cum_payoffs for p in self.players}

    def __init__(self, *args, **kwargs):
        super().__init__(['game_settings'], *args, **kwargs)
    
    def play(self):
        actions = [p.strategy() for p in self.players]
        [p.actions.append(a) for p, a in zip(self.players, actions)]
        payoffs = self.payoff_function()
        for p in self.players:
            p.payoffs.append(payoffs[p.name])
            cum_payoff = p.cum_payoffs[-1] if p.cum_payoffs else 0
            p.cum_payoffs.append(cum_payoff + payoffs[p.name])
        self.rounds += 1
    
    def html_table(self):
        return HTML_TABLE.format(game=self)

    @property
    def _players(self):
        return ''.join([PLAYER.format(name=p.name) for p in self.players])
    
    @property
    def _stats_header(self):
        return ''.join([STATS_HEADER for i in self.players])

    @property
    def _stats(self):
        stats = ''
        for i in range(self.rounds):
            self._round = i
            stats += ROUND_STATS.format(game=self)
        return stats

    @property
    def _player_stats(self):
        return ''.join([
            PLAYER_STATS.format(
                action=p.actions[self._round],
                payoff=p.payoffs[self._round],
                cum_payoff=p.cum_payoffs[self._round]
            ) 
            for p in self.players
        ])



class PlayerMixin(Base):
    index = Column(Integer)
    name = Column(String)
    actions = Column(MutableListType)
    payoffs = Column(MutableListType)
    cum_payoffs = Column(MutableListType)

    @declared_attr
    def game_id(cls):
        return Column(Integer, ForeignKey('game.id'))

    @declared_attr
    def strategy(cls):
        return relationship(
            'Strategy', 
            backref='player',
            uselist=False
        )

    def __init__(self, game=None, *args, **kwargs):
        self.actions, self.payoffs, self.cum_payoffs = [], [], []
        super().__init__(['player_settings'], game=game, *args, **kwargs)


class StrategyMixin(FunctionMixin, Base):
    @declared_attr
    def player_id(cls):
        return Column(Integer, ForeignKey('player.id'))

    @property
    def parent(self):
        return self.player

    @parent.setter
    def parent(self, player):
        self.player = player


class PayoffMixin(FunctionMixin, Base):
    @declared_attr
    def game_id(cls):
        return Column(Integer, ForeignKey('game.id'))

    @property
    def parent(self):
        return self.game

    @parent.setter
    def parent(self, game):
        self.game = game


HTML_TABLE = """
<table class="table table-striped text-center">
    <thead>
        <tr>
            <th></th>
            {game._players}
        </tr>
        <tr>
            <th scope="col">Round</th>
            {game._stats_header}
        </tr>
    </thead>
    <tbody>
        {game._stats}
    </tbody>
</table>
"""

PLAYER = '<th scope="col" colspan="3">{name}</th>'

STATS_HEADER = """
<th scope="col">Action</th>
<th scope="col">Payoff</th>
<th scope="col">Cumulative Payoff</th>
"""

ROUND_STATS = """
<tr>
    <td>{game._round}</td>
    {game._player_stats}
</tr>
"""

PLAYER_STATS = """
<td>{action}</td>
<td>{payoff}</td>
<td>{cum_payoff}</td>
"""