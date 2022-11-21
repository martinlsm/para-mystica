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


class ActionError(Exception):
    '''Factions raise this exception when an action is disallowed
    at a given state.'''
    pass


class LogicalError(Exception):
    '''Fatal logical error that should not be caught'''
    pass
