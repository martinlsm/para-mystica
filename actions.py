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


# Returns a list with the number of resources before each round 1-6
# and post-game resources as the last element in the list.
def process_actions(faction, action_list):
    round_resources = []
    print(action_list)

    # Pad the list in case there are missing go-to-next-round actions.
    num_next_rounds = action_list.count(Action.NEXT_ROUND)
    action_list.extend([Action.NEXT_ROUND] * (6 - num_next_rounds))
    print(action_list)

    # Proceed to Round 1 unconditionally.
    _resolve(faction, Action.NEXT_ROUND)

    for action in action_list:
        _resolve(faction, action)
        if action == Action.NEXT_ROUND:
            round_resources.append(faction.resources)

    print(round_resources)
    return round_resources


def _resolve(faction, action):
    match action:
        case Action.NEXT_ROUND:
            faction.next_round()
        case Action.UPGRADE_DIGGING:
            faction.upgrade_digging()
        case Action.UPGRADE_SHIPPING:
            faction.upgrade_shipping()
        case Action.DIG:
            # TODO: Fix digging with multiple spades
            faction.dig(1)
        case Action.BUILD_DWELLING:
            faction.build_dwelling()
        case Action.UPGRADE_TO_TP:
            # TODO: Fix upgrading without neighbor
            faction.upgrade_to_tp()
        case Action.UPGRADE_TO_TE:
            faction.upgrade_to_te()
        case Action.UPGRADE_TO_SA:
            faction.upgrade_to_sa()
        case Action.UPGRADE_TO_SH:
            faction.upgrade_to_sh()
        case Action.TUNNELING:
            faction.tunnel()
        case other:
            raise ValueError(f'Could not resolve unknown action {action}')
