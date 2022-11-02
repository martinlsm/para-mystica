import tkinter as tk

from actions import Action

def action_button_create(app_ctrl, master, action, grid_row, grid_col):
    match action:
        case Action.UPGRADE_DIGGING:
            return UpgradeDiggingButton(app_ctrl, master, grid_row, grid_col)
        case Action.UPGRADE_SHIPPING:
            return UpgradeShippingButton(app_ctrl, master, grid_row, grid_col)
        case Action.DIG:
            return DigButton(app_ctrl, master, grid_row, grid_col)
        case Action.BUILD_DWELLING:
            return BuildDwellingButton(app_ctrl, master, grid_row, grid_col)
        case Action.UPGRADE_TO_TP:
            return UpgradeToTPButton(app_ctrl, master, grid_row, grid_col)
        case Action.UPGRADE_TO_TE:
            return UpgradeToTEButton(app_ctrl, master, grid_row, grid_col)
        case Action.UPGRADE_TO_SA:
            return UpgradeToSAButton(app_ctrl, master, grid_row, grid_col)
        case Action.UPGRADE_TO_SH:
            return UpgradeToSHButton(app_ctrl, master, grid_row, grid_col)
        case Action.TUNNELING:
            return TunnelingButton(app_ctrl, master, grid_row, grid_col)
        case other:
            raise ValueError(f'Invalid Action enum: {action}')


class ActionButton:
    def __init__(self, app_ctrl, master, label, action, grid_row, grid_col):
        self.app_ctrl = app_ctrl
        self.label = label
        self.action = action

        btn = tk.Button(master, text=label, command=self._on_press)
        btn.grid(row=grid_row, column=grid_col)


    def _on_press(self):
        print(f'Pressed "{self.label}"')
        self.app_ctrl.append_game_event(self.label, self.action)
        self.app_ctrl.update_round_displays()


class UpgradeDiggingButton:
    def __init__(self, app_ctrl, master, grid_row, grid_col):
        ActionButton(app_ctrl, master, 'Upgrade Digging', Action.UPGRADE_DIGGING, grid_row, grid_col)


class UpgradeShippingButton:
    def __init__(self, app_ctrl, master, grid_row, grid_col):
        ActionButton(app_ctrl, master, 'Upgrade Shipping', Action.UPGRADE_SHIPPING, grid_row, grid_col)


class DigButton:
    def __init__(self, app_ctrl, master, grid_row, grid_col):
        ActionButton(app_ctrl, master, 'Dig', Action.DIG, grid_row, grid_col)


class BuildDwellingButton:
    def __init__(self, app_ctrl, master, grid_row, grid_col):
        ActionButton(app_ctrl, master, 'Build Dwelling', Action.BUILD_DWELLING, grid_row, grid_col)


class UpgradeToTPButton:
    def __init__(self, app_ctrl, master, grid_row, grid_col):
        ActionButton(app_ctrl, master, 'Upgrade to Trading Post', Action.UPGRADE_TO_TP,
                     grid_row, grid_col)


class UpgradeToTEButton:
    def __init__(self, app_ctrl, master, grid_row, grid_col):
        ActionButton(app_ctrl, master, 'Upgrade to Temple', Action.UPGRADE_TO_TE, grid_row, grid_col)


class UpgradeToSAButton:
    def __init__(self, app_ctrl, master, grid_row, grid_col):
        ActionButton(app_ctrl, master, 'Upgrade to Sanctuary', Action.UPGRADE_TO_SA, grid_row,
                     grid_col)


class UpgradeToSHButton:
    def __init__(self, app_ctrl, master, grid_row, grid_col):
        ActionButton(app_ctrl, master, 'Upgrade to Stronghold', Action.UPGRADE_TO_SH, grid_row,
                     grid_col)


class TunnelingButton:
    def __init__(self, app_ctrl, master, grid_row, grid_col):
        ActionButton(app_ctrl, master, 'Tunneling', Action.TUNNELING, grid_row, grid_col)
