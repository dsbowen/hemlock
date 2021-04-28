import numpy as np
import pandas as pd
from flask_login import current_user
from hemlock import Participant
from hemlock.tools import get_data

from itertools import cycle, product
from math import ceil
from random import shuffle

class SuccessiveRejectionsAssigner:
    def __init__(self, conditions, target, total_participants):
        self.conditions = conditions
        self.keys = list(conditions.keys())
        self.arms = list(product(*conditions.values()))
        shuffle(self.arms)
        self.remaining_arms = self.arms.copy()
        self.arms_cycle = cycle(self.remaining_arms)
        self.target = target
        self.total_participants = total_participants

        K = len(self.arms)
        logK = .5 + sum([1/i for i in range(2, K+1)])
        n_k = np.array([
            ceil(1/logK * (total_participants-K)/(K+1-i))
            for i in range(1, K)
        ])
        # total number of participants in each phase
        n_k = np.diff(np.insert(n_k, 0, 0)) * np.arange(K, 1, step=-1)
        # add extra participants (rounding error) to phase 1
        n_k[0] += total_participants - n_k.sum() 
        # number of participants at the end of each phase
        self.n_k = n_k.cumsum()

    def next(self, participant=None):
        def remove_worst_arm():
            df = pd.DataFrame(get_data())
            df[self.target] = pd.to_numeric(df[self.target])
            y_mean = df.groupby(self.keys)[self.target].mean().sort_values().reset_index()
            sorted_arms = y_mean[self.keys].values
            i, arm_removed = 0, False
            while not arm_removed:
                worst_arm = tuple(sorted_arms[i])
                if worst_arm in self.remaining_arms:
                    self.remaining_arms.remove(worst_arm)
                    arm_removed = True
                i += 1
            self.arms_cycle = cycle(self.remaining_arms)

        participants = Participant.query.filter_by(_completed=True).all()
        curr_phase = len(self.arms) - len(self.remaining_arms)
        if (
            len(self.arms) > 2 
            and len(participants) > self.n_k[curr_phase]
        ):
            remove_worst_arm()
        assignment = {
            key: val for key, val in zip(self.keys, next(self.arms_cycle))
        }
        participant = participant or current_user
        participant.meta.update(assignment)
        # try:
        #     participant = participant or current_user
        #     participant.meta.update(assignment)
        # except:
        #     print('Unable to update participant metadata.')
        return assignment
