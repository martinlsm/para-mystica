import tkinter as tk

import actions

from action_buttons import action_button_create

from factions import faction_names, create_faction

from resources import Resources


# This object can be passed around to GUI components that want to
# signal updates to the overall GUI.
class AppController:
    def __init__(self, app):
        self.app = app

    def select_faction(self, faction_name):
        self.app.select_faction(faction_name)

    def append_game_event(self, text):
        self.app.append_game_event(text)


class App:
    def __init__(self):
        self.root = tk.Tk()

        FactionSelector(self.root, AppController(self))
        self.game_event_seq = GameEventSequence(self.root)
        self.resource_displays = ResourceDisplayList(self.root)

        self.active_faction = None
        self.action_selector = None

    def run(self):
        self.root.mainloop()

    def select_faction(self, faction_name):
        if self.active_faction is not None:
            self.action_selector.destroy()

        self.active_faction = create_faction(faction_name)

        self.action_selector = ActionSelector(self.root, AppController(self),
                                              self.active_faction)

    def append_game_event(self, text):
        self.game_event_seq.append(text)


class FactionSelector:
    def __init__(self, master, app_ctrl):
        self.app_ctrl = app_ctrl

        self.selection = tk.StringVar()
        self.selection.set('Choose Faction')
        self.selection.trace('w', self._selection_callback)

        self.dropdown_menu = tk.OptionMenu(master, self.selection,
                                           *faction_names())
        self.dropdown_menu.grid(sticky=tk.NW)

    def _selection_callback(self, *args):
        self.app_ctrl.select_faction(self.selection.get())


# XXX: Rename
class ActionSelector:
    def __init__(self, master, app_ctrl, faction):
        self.app_ctrl = app_ctrl

        self.frame = tk.Frame(master)
        self.frame.grid(sticky=tk.S)

        self.act_btns = []
        self.grid_width = 5

        for action in actions.actions_list(faction):
            self._add_action_button(action)

    def destroy(self):
        self.frame.destroy()

    def _add_action_button(self, action):
        grid_row = len(self.act_btns) // 5
        grid_col = len(self.act_btns) % self.grid_width

        btn = action_button_create(self.app_ctrl, self.frame, action, grid_row,
                                   grid_col)
        self.act_btns.append(btn)


class GameEventSequence:
    def __init__(self, master):
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE,
                                  activestyle=tk.NONE)
        self.listbox.grid(sticky=tk.W)

        # Left click
        self.listbox.bind('<Button-1>', self._select_item)
        # Left click release
        self.listbox.bind('<ButtonRelease-1>', self._unselect_item)
        # Drag mouse
        self.listbox.bind('<B1-Motion>', self._shift_selection)

        self.selected_idx = None

    def append(self, text):
        self.listbox.insert(tk.END, text)

    def _select_item(self, event):
        self.selected_idx = self.listbox.nearest(event.y)

    def _unselect_item(self, event):
        self.listbox.select_clear(self.selected_idx)

    def _shift_selection(self, event):
        new_idx = self.listbox.nearest(event.y)
        old_idx = self.selected_idx

        if new_idx < old_idx:
            item_to_push_down = self.listbox.get(new_idx)
            self.listbox.delete(new_idx)
            self.listbox.insert(new_idx + 1, item_to_push_down)
            self.selected_idx = new_idx
        elif new_idx > old_idx:
            item_to_push_up = self.listbox.get(new_idx)
            self.listbox.delete(new_idx)
            self.listbox.insert(new_idx - 1, item_to_push_up)
            self.selected_idx = new_idx


class ResourceDisplayList:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.grid(sticky=tk.E)

        self.displays = [ResourceDisplay(frame, row, 0)
                         for row in range(0, 7)]

        # XXX: Remove this
        for display in self.displays:
            display.set_resources(Resources())

    def update(resources_list):
        for i,display in enumerate(self.displays):
            display.set_resources(resources_list[i])


class ResourceDisplay:
    def __init__(self, master, row, col):
        self.resources = Resources()
        frame = tk.Frame(master)
        frame.grid(sticky=tk.E)
        self.text = tk.Label(frame)
        self.text.grid(row=row, column=col)

    def set_resources(self, resources):
        self.resources = resources.copy()
        self.text.config(text=f'W: {self.resources.w}, ' +
                         f'G: {self.resources.g}, ' +
                         f'P: {self.resources.p}')


if __name__ == '__main__':
    App().run()
