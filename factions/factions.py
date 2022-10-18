from factions import *

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
