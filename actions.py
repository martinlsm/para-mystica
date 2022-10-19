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


def actions_list(faction):
    possible_actions = faction.supported_actions.union({Action.NEXT_ROUND})

    for act in Action:
        if act in possible_actions:
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

