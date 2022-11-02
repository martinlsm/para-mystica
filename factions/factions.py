from factions import *

from actions import Action

# XXX: Sort these alphabetically
def faction_names():
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
