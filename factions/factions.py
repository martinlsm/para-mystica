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

def list_actions(faction_name):
    match faction_name:
        case 'Dwarves':
            supported_actions = Dwarves.supported_actions
        case other:
            raise ValueError(f'Uknown faction "{faction_name}"')

    possible_actions = supported_actions.union({Action.NEXT_ROUND})

    for act in Action:
        if act in possible_actions:
            yield act
