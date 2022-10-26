from resources import Resources
from actions import Action

class Dwarves:
    starting_resources = Resources(w=3, g=15)

    dwelling_income = [Resources(w=1),  # 0 D
                       Resources(w=2),  # 1 D
                       Resources(w=3),  # .
                       Resources(w=4),  # .
                       Resources(w=5),  # .
                       Resources(w=6),
                       Resources(w=7),
                       Resources(w=8),
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

    num_starting_dwellings = 2

    dwelling_cost = Resources(w=1, g=2)
    tp_cost_with_adj = Resources(w=2, g=3)
    tp_cost_no_adj = Resources(w=2, g=6)
    te_cost = Resources(w=2, g=5)
    sa_cost = Resources(w=4, g=6)
    sh_cost = Resources(w=4, g=6)

    max_level_digging = 3
    upgrade_digging_cost = Resources(w=2, g=5, p=1)

    # Fields set to None because dwarves do not have shipping
    start_level_shipping = None
    max_level_shipping = None
    upgrade_shipping_cost = None

    supported_actions = {
        Action.UPGRADE_DIGGING,
        Action.DIG,
        Action.BUILD_DWELLING,
        Action.UPGRADE_TO_TP,
        Action.UPGRADE_TO_TE,
        Action.UPGRADE_TO_SA,
        Action.UPGRADE_TO_SH,
        Action.TUNNELING,
    }

    def __init__(self):
        self.resources = Dwarves.starting_resources.copy()
        self.num_dwellings = Dwarves.num_starting_dwellings
        self.num_tp = 0
        self.num_te = 0
        self.num_sa = 0
        self.num_sh = 0
        self.digging_level = 1

        # Faction-specific attributes
        self.tunneling_worker_cost = 2

    def next_round(self):
        self.resources += Dwarves.dwelling_income[self.num_dwellings] + \
                          Dwarves.tp_income[self.num_tp] + \
                          Dwarves.te_income[self.num_te] + \
                          Dwarves.sa_income[self.num_sa] + \
                          Dwarves.sh_income[self.num_sh]

    def build_dwelling(self):
        assert self.num_dwellings < 8

        self.num_dwellings += 1
        self.resources -= Dwarves.dwelling_cost

    def upgrade_to_tp(self, adj_opponent):
        assert self.num_tp < 4
        assert self.num_dwellings > 0

        self.num_dwellings -= 1
        self.num_tp += 1
        if adj_opponent:
            self.resources -= Dwarves.tp_cost_with_adj
        else:
            self.resources -= Dwarves.tp_cost_no_adj

    def upgrade_to_te(self):
        assert self.num_te < 3
        assert self.num_tp > 0
        self.num_tp -= 1
        self.num_te += 1
        self.resources -= Dwarves.te_cost

    def upgrade_to_sa(self):
        assert self.num_sa < 1
        assert self.num_te > 0
        self.num_te -= 1
        self.num_sa += 1
        self.resources -= Dwarves.sa_cost

    def upgrade_to_sh(self):
        assert self.num_sh < 1
        assert self.num_tp > 0
        self.num_tp -= 1
        self.num_sh += 1
        self.tunneling_worker_cost = 1
        self.resources -= Dwarves.sh_cost

    def upgrade_digging(self):
        assert self.digging_level >= 1
        assert self.digging_level < Dwarves.max_level_digging
        self.digging_level += 1
        self.resources -= self.upgrade_digging_cost

    def dig(self, num_spades):
        cost_per_spade = Resources(w=(4 - self.digging_level))
        self.resources -= cost_per_spade * num_spades

    def upgrade_shipping(self):
        raise ValueError('Dwarves do not have shipping')

    def tunnel(self):
        self.resources -= Resources(w=self.tunneling_worker_cost)
