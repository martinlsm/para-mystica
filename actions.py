from enum import Enum

class Action(Enum):
    NEXT_ROUND = 0

    UPGRADE_DIGGING = 1
    UPGRADE_SHIPPING = 2
    DIG = 3
    BUILD_DWELLING = 4
    UPGRADE_TO_TP = 5
    UPGRADE_TO_TE = 6
    UPGRADE_TO_SA = 7
    UPGRADE_TO_SH = 8

    TUNNELING = 9


# class NextRound:
#     def resolve(self, faction):
#         faction.next_round()
# 
# class UpgradeDigging:
#     def resolve(self, faction):
#         faction.upgrade_digging()
# 
# class UpgradeShipping:
#     def resolve(self, faction):
#         self.faction.upgrade_shipping()
# 
# class Dig:
#     def __init__(self, num_spades):
#         self.num_spades = num_spades
# 
#     def resolve(self, faction):
#         faction.dig(num_spades)
# 
# class BuildDwelling:
#     def resolve(self, faction):
#         faction.build_dwelling()
# 
# class UpgradeToTP:
#     def resolve(self, faction):
#         faction.upgrade_to_tp()
# 
# class UpgradeToTE:
#     def resolve(self, faction):
#         faction.upgrade_to_te()
# 
# class UpgradeToSA:
#     def resolve(self, faction):
#         faction.upgrade_to_sa()
# 
# class UpgradeToSH:
#     def resolve(self, faction):
#         faction.upgrade_to_sh()
# 
# class Tunneling:
#     def resolve(self, faction):
#         faction.tunneling()

def actions_list(faction):
    for act in Action:
        if act in faction.supported_actions:
            yield act


# Returns a list with the number of resources before each round 1-6
# and post-game resources as the last element in the list.
def process_actions(faction, action_list):
    round_resources = []

    # XXX: This logic might need to change
    assert type(round_resources[0]) == NextRound
    assert type(round_resources[-1]) == NextRound

    for action in action_list:
        action.resolve(faction)
        if type(action) == NextRound:
            round_resources.append(faction.resources)

    assert len(round_resources) == 7 

    return round_resources

