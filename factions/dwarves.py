from copy import deepcopy

from actions import Action, ActionError, LogicalError
from factions.building_delegate import BuildingDelegate
from resources import Resources

class Dwarves:
    starting_resources = Resources(w=3, g=15)

    dwelling_income = [Resources(w=1),  # 0 D
                       Resources(w=2),  # 1 D
                       Resources(w=3),  # 2 D
                       Resources(w=4),  # 3 D
                       Resources(w=5),  # 4 D
                       Resources(w=6),  # 5 D
                       Resources(w=7),  # 6 D
                       Resources(w=8),  # 7 D
                       Resources(w=8)]  # 8 D

    tp_income = [Resources(),      # 0 TP
                 Resources(g=3),   # 1 TP
                 Resources(g=5),   # 2 TP
                 Resources(g=7),   # 3 TP
                 Resources(g=10)]  # 4 TP

    te_income = [Resources(),     # 0 TE
                 Resources(p=1),  # 1 TE
                 Resources(p=2),  # 2 TE
                 Resources(p=3)]  # 3 TE

    sa_income = [Resources(),     # 0 SA
                 Resources(p=1)]  # 1 SA

    sh_income = [Resources(),  # 0 SH
                 Resources()]  # 1 SH

    max_level_digging = 3
    upgrade_digging_cost = Resources(w=2, g=5, p=1)

    # Fields set to None because dwarves do not have shipping
    start_level_shipping = None
    max_level_shipping = None
    upgrade_shipping_cost = None

    supported_actions = [
        Action.BUILD_DWELLING,
        Action.DIG,
        Action.UPGRADE_TO_TP,
        Action.UPGRADE_TO_TE,
        Action.UPGRADE_TO_SA,
        Action.UPGRADE_TO_SH,
        Action.UPGRADE_DIGGING,
        Action.TUNNELING,
    ]

    def __init__(self):
        self.resources = Dwarves.starting_resources.copy()
        self.digging_level = 1

        # Faction-specific attributes
        self.tunneling_worker_cost = 2

        self.building_delegate = BuildingDelegate()

    def __str__(self):
        return f'Dwarves({self.resources})'

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return deepcopy(self)

    def get_resources(self):
        return self.resources

    def next_round(self):
        self.resources += Dwarves.dwelling_income[self.building_delegate.num_dwellings] + \
                          Dwarves.tp_income[self.building_delegate.num_tp] + \
                          Dwarves.te_income[self.building_delegate.num_te] + \
                          Dwarves.sa_income[self.building_delegate.num_sa] + \
                          Dwarves.sh_income[self.building_delegate.num_sh]

    def build_dwelling(self):
        self.resources = self.building_delegate.build_dwelling(self.resources)

    def build_trading_post(self, adj_opponent):
        self.resources = self.building_delegate.build_trading_post(self.resources,
                                                                   adj_opponent)

    def build_temple(self):
        self.resources = self.building_delegate.build_temple(self.resources)

    def build_sanctuary(self):
        self.resources = self.building_delegate.build_sanctuary(self.resources)

    def build_stronghold(self):
        self.resources = self.building_delegate.build_stronghold(self.resources)

    def upgrade_digging(self):
        if self.digging_level >= Dwarves.max_level_digging:
            raise ActionError('Digging is already upgraded to maximum ' +
                              f'({Dwarves.max_level_digging})')

        self.digging_level += 1
        self.resources -= self.upgrade_digging_cost

    def dig(self, num_spades):
        cost_per_spade = Resources(w=(4 - self.digging_level))
        self.resources -= cost_per_spade * num_spades

    def upgrade_shipping(self):
        raise LogicalError('Dwarves do not have shipping')

    def tunnel(self):
        self.resources -= Resources(w=self.tunneling_worker_cost)
