import tkinter as tk

import actions 

from action_buttons import action_button_create

from factions import Dwarves
from factions import faction_names, create_faction


class App:
    def __init__(self):
        self.root = tk.Tk()

        FactionSelector(self)
        ActionSequence(self)

        self.active_faction = None
        self.action_selector = None


    def run(self):
        self.root.mainloop()


    def select_faction(self, faction_name):
        if self.active_faction is not None:
            self.action_selector.destroy()

        self.active_faction = create_faction(faction_name)

        self.action_selector = ActionSelector(self, self.active_faction)


class FactionSelector:
    def __init__(self, app):
        self.app = app

        self.selection = tk.StringVar()
        self.selection.set('Choose Faction')
        self.selection.trace('w', self._selection_callback)

        self.dropdown_menu = tk.OptionMenu(app.root, self.selection, *faction_names())
        self.dropdown_menu.grid(sticky=tk.NW)


    def _selection_callback(self, *args):
        self.app.select_faction(self.selection.get())


class ActionSelector:
    def __init__(self, app, faction):
        self.frame = tk.Frame(app.root)
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

        btn = action_button_create(action, self.frame, grid_row, grid_col)
        self.act_btns.append(btn)


class ActionSequence:
    def __init__(self, app):
        self.listbox = tk.Listbox(app.root, selectmode=tk.SINGLE, activestyle=tk.NONE)

        # Left click
        self.listbox.bind('<Button-1>', self._select_item)
        # Left click release
        self.listbox.bind('<ButtonRelease-1>', self._unselect_item)
        # Drag mouse
        self.listbox.bind('<B1-Motion>', self._shift_selection)

        self.selected_idx = None

        # XXX: Temp stuff
        for i,name in enumerate(['name'+str(i) for i in range(10)]):
            self.listbox.insert(tk.END, name)

        self.listbox.grid(sticky=tk.W)


    def append_item(self, text):
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


if __name__ == '__main__':
    App().run()
