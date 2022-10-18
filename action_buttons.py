import tkinter as tk

from actions import Action

def action_button_create(action, master, grid_row, grid_col):
    match action:
        case Action.NEXT_ROUND:
            return NextRoundButton(master, grid_row, grid_col)
        case Action.UPGRADE_DIGGING:
            return UpgradeDiggingButton(master, grid_row, grid_col)
        case Action.UPGRADE_SHIPPING:
            return UpgradeShippingButton(master, grid_row, grid_col)
        case Action.DIG:
            return DigButton(master, grid_row, grid_col)
        case Action.BUILD_DWELLING:
            return BuildDwellingButton(master, grid_row, grid_col)
        case Action.UPGRADE_TO_TP:
            return UpgradeToTPButton(master, grid_row, grid_col)
        case Action.UPGRADE_TO_TE:
            return UpgradeToTEButton(master, grid_row, grid_col)
        case Action.UPGRADE_TO_SA:
            return UpgradeToSAButton(master, grid_row, grid_col)
        case Action.UPGRADE_TO_SH:
            return UpgradeToSHButton(master, grid_row, grid_col)
        case Action.TUNNELING:
            return TunnelingButton(master, grid_row, grid_col)
        case other:
            raise ValueError(f'Invalid Action enum: {action}')


class NextRoundButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Next Round', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the next round button')


class UpgradeDiggingButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Upgrade Digging', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the upgrade digging button')


class UpgradeShippingButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Upgrade Shipping', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the upgrade shipping button')


class DigButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Dig', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the dig button')


class BuildDwellingButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Build Dwelling', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the build dwelling button')


class UpgradeToTPButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Upgrade to Trading Post', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the upgrade to trading post button')


class UpgradeToTEButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Upgrade to Temple', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the upgrade to temple button')


class UpgradeToSAButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Upgrade to Sanctuary', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the upgrade to sanctuary button')


class UpgradeToSHButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Upgrade to Stronghold', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the upgrade to stronghold button')


class TunnelingButton:
    def __init__(self, master, grid_row, grid_col):
        btn = tk.Button(master, text='Tunneling', command=self.on_press)
        btn.grid(row=grid_row, column=grid_col)

    def on_press(self):
        print('Pressed the tunneling button')
