from abc import ABC

from actions import ActionError
from resources import Resources

class BuildingDelegate:
    def __init__(self, num_starting_dwellings=2,
                 dwelling_cost=Resources(w=1, g=2),
                 tp_cost_with_adj=Resources(w=2, g=3),
                 tp_cost_no_adj=Resources(w=2, g=6),
                 te_cost=Resources(w=2, g=5),
                 sa_cost=Resources(w=4, g=6),
                 sh_cost=Resources(w=4, g=6)):
        self.num_dwellings = num_starting_dwellings
        self.num_tp = 0
        self.num_te = 0
        self.num_sa = 0
        self.num_sh = 0

        self.dwelling_cost = dwelling_cost.copy()
        self.tp_cost_with_adj = tp_cost_with_adj.copy()
        self.tp_cost_no_adj = tp_cost_no_adj.copy()
        self.te_cost = te_cost.copy()
        self.sa_cost = sa_cost.copy()
        self.sh_cost = sh_cost.copy()

    def build_dwelling(self, resources):
        if self.num_dwellings >= 8:
            raise ActionError('Number of dwellings are at maximum (8)')

        self.num_dwellings += 1

        return resources - self.dwelling_cost

    def build_trading_post(self, resources, adj_opponent):
        if self.num_tp >= 4:
            raise ActionError('Number of trading posts are at maximum (4)')
        if self.num_dwellings == 0:
            raise ActionError('No placed dwelling to upgrade')

        self.num_dwellings -= 1
        self.num_tp += 1

        if adj_opponent:
            return resources - self.tp_cost_with_adj
        else:
            return resources - self.tp_cost_no_adj

    def build_temple(self, resources):
        if self.num_te >= 3:
            raise ActionError('Number of temples are at maximum (3)')
        if self.num_tp == 0:
            raise ActionError('No trading post available for upgrade')

        self.num_tp -= 1
        self.num_te += 1

        return resources - self.te_cost

    def build_sanctuary(self, resources):
        if self.num_sa >= 1:
            raise ActionError('Sanctuary is already built')
        if self.num_te == 0:
            raise ActionError('No temple available for upgrade')

        self.num_te -= 1
        self.num_sa += 1

        return resources - self.sa_cost

    def build_stronghold(self, resources):
        if self.num_sh >= 1:
            raise ActionError('Stronghold is already built')
        if self.num_tp == 0:
            raise ActionError('No trading posts available for upgrade')

        self.num_tp -= 1
        self.num_sh += 1
        self.tunneling_worker_cost = 1

        return resources - self.sh_cost
