from enum import Enum

class Action(Enum):
    UPGRADE_DIGGING = 1
    UPGRADE_SHIPPING = 2
    DIG = 3
    BUILD_DWELLING = 4
    UPGRADE_TO_TP = 5
    UPGRADE_TO_TE = 6
    UPGRADE_TO_SA = 7
    UPGRADE_TO_SH = 8

    TUNNELING = 9


def process_actions(faction, action_lists):
    assert(len(action_lists) == 6)

    # action_list = [[R1 actions], [R2 actions], ..., [R6 actions]]
    # round_resource = [(before R1, after R1), (before R2, after R2),
    #                   ..., (before R6, after R6)
    round_resources = []

    for action_list in action_lists:
        before_round_res = faction.get_resources()
        for action in action_list:
            _resolve(faction, action)
        after_round_res = faction.get_resources()

        round_resources.append((before_round_res, after_round_res))

    return round_resources


def _resolve(faction, action):
    match action:
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
            faction.upgrade_to_tp(True)
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
