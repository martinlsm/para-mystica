from factions import *

from actions import Action

def faction_names():
    # TODO: Sort these alphabetically
    factions = [
        'Dwarves',
    ]

    for faction in factions:
        yield faction


def create_faction(faction_name):
    match faction_name:
        case 'Dwarves':
            return Dwarves()


def supported_actions(faction_name):
    match faction_name:
        case 'Dwarves':
            return Dwarves.supported_actions.copy()
        case other:
            raise ValueError(f'Unknown faction "{faction_name}"')


def next_round(faction_state):
    next_state = faction_state.copy()
    next_state.next_round()
    return next_state


def process_actions(faction_state, actions):
    next_state = faction_state.copy()

    for action in actions:
        resolve_action(next_state, action)

    return next_state


def resolve_action(faction, action):
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
            faction.build_trading_post(True)
        case Action.UPGRADE_TO_TE:
            faction.build_temple()
        case Action.UPGRADE_TO_SA:
            faction.build_sanctuary()
        case Action.UPGRADE_TO_SH:
            faction.build_stronghold()
        case Action.TUNNELING:
            faction.tunnel()
        case other:
            raise ValueError(f'Could not resolve unknown action {action}')
