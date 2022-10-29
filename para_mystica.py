import tkinter as tk

import actions

from action_buttons import action_button_create

from factions import faction_names, create_faction, list_actions

from resources import Resources


class AppController:
    '''
    This object can be passed around to GUI components that want to
    signal updates to the overall GUI.
    '''

    def __init__(self, app):
        self.app = app

    def select_faction(self, faction_name):
        self.app.select_faction(faction_name)

    def select_active_round(self, round_num):
        print(f'Selected round {round_num}')
        self.app.select_active_round(round_num)

    def append_game_event(self, text, action):
        self.app.append_game_event(text, action)

    def update_resource_displays(self):
        self.app.update_resource_displays()


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Para Mystica')

        FactionSelector(self.root, AppController(self))

        self.round_displays = RoundInfoDisplayList(self.root)

        self.active_round_selector = ActiveRoundSelector(AppController(self), self.root)

        self.active_faction = None
        self.action_selector = None
        self.active_round = None

    def run(self):
        self.root.mainloop()

    def select_faction(self, faction_name):
        if self.active_faction is not None:
            self.action_selector.destroy()

        self.active_faction = faction_name

        self.action_selector = ActionSelector(self.root, AppController(self),
                                              self.active_faction)

    def append_game_event(self, text, action):
        self.game_event_seq.append(text, action)

    def update_resource_displays(self):
        faction = create_faction(self.active_faction)
        acts = self.game_event_seq.get_actions()
        resource_list = actions.process_actions(faction, acts)
        self.resource_displays.update(resource_list)

    def select_active_round(self, round_num):
        self.active_round = round_num


class FactionSelector:
    def __init__(self, master, app_ctrl):
        self.app_ctrl = app_ctrl

        self.selection = tk.StringVar()
        self.selection.set('Choose Faction')
        self.selection.trace('w', self._selection_callback)

        self.dropdown_menu = tk.OptionMenu(master, self.selection,
                                           *faction_names())
        self.dropdown_menu.pack()

    def _selection_callback(self, *args):
        self.app_ctrl.select_faction(self.selection.get())


class ActionSelector:
    def __init__(self, master, app_ctrl, faction):
        self.app_ctrl = app_ctrl

        self.frame = tk.Frame(master)
        self.frame.pack()

        self.act_btns = []
        self.grid_width = 5

        for action in list_actions(faction):
            self._add_action_button(action)

    def destroy(self):
        self.frame.destroy()

    def _add_action_button(self, action):
        grid_row = len(self.act_btns) // 5
        grid_col = len(self.act_btns) % self.grid_width

        btn = action_button_create(self.app_ctrl, self.frame, action, grid_row,
                                   grid_col)
        self.act_btns.append(btn)


# TODO: Rename
class RoundFrame:
    def __init__(self, master, label, row, col):
        frame = tk.Frame(master)
        frame.grid(row=row, column=col)

        self.label = tk.Label(frame, text=label)
        self.label.pack()

        self.event_sequence = GameEventSequence(frame)

        self.round_info_display = RoundInfoDisplay(frame)

        # TODO: Might delete this later.
        self.round_info_display.update(Resources(), Resources())


class GameEventSequence:
    def __init__(self, master):
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE,
                                  activestyle=tk.NONE)
        self.listbox.pack()

        # Left click
        self.listbox.bind('<Button-1>', self._select_item)
        # Left click release
        self.listbox.bind('<ButtonRelease-1>', self._unselect_item)
        # Drag mouse
        self.listbox.bind('<B1-Motion>', self._shift_selection)

        # Unfortunately, Tkinter does not seem to support storing metadata of
        # its elements; they need to be plain strings. This list is therefore
        # used to store the corresponding action of each element in the
        # listbox and it needs to be mirroring self.listbox at all times.
        self.list_actions = []

        self.selected_idx = None

    def append(self, text, action):
        self.listbox.insert(tk.END, text)
        self.list_actions.append(action)

    def get_actions(self):
        return self.list_actions.copy()

    def _select_item(self, event):
        self.selected_idx = self.listbox.nearest(event.y)

    def _unselect_item(self, event):
        self.listbox.select_clear(self.selected_idx)

    def _shift_selection(self, event):
        new_idx = self.listbox.nearest(event.y)
        old_idx = self.selected_idx

        if new_idx < old_idx:
            # Swap the two elements.
            item_to_push_down = self.listbox.get(new_idx)
            self.listbox.delete(new_idx)
            self.listbox.insert(new_idx + 1, item_to_push_down)

            # Do the same with the mirrored list of actions.
            item_to_push_down = self.action_list[new_idx]
            self.action_list.pop(new_idx)
            self.action_list.insert(new_idx + 1, item_to_push_down)

            self.selected_idx = new_idx
        elif new_idx > old_idx:
            # Swap the two elements.
            item_to_push_up = self.listbox.get(new_idx)
            self.listbox.delete(new_idx)
            self.listbox.insert(new_idx - 1, item_to_push_up)

            # Do the same with the mirrored list of actions.
            item_to_push_up = self.action_list(new_idx)
            self.action_list.delete(new_idx)
            self.action_list.insert(new_idx - 1, item_to_push_up)

            self.selected_idx = new_idx


# TODO: Rename
class RoundInfoDisplayList:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()

        self.round_events = \
                [RoundFrame(frame, f'Round {col + 1}', 0, col) \
                    for col in range(0, 6)]



# TODO: Rename
class RoundInfoDisplay:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()

        self.res_before = tk.Label(frame)
        self.res_before.grid(row=0, column=0)

        self.res_after = tk.Label(frame)
        self.res_after.grid(row=1, column=0)

    def update(self, res_before, res_after):
        self.res_before.config(text=f'Before: W: {res_before.w}, G: {res_before.g}, P: {res_before.p}')
        self.res_after.config(text=f'After: W: {res_after.w}, G: {res_after.g}, P: {res_after.p}')


class ActiveRoundSelector:
    def __init__(self, app_ctrl, master):
        self.app_ctrl = app_ctrl

        self.selection = tk.StringVar()
        self.selection.set('Select Round')
        self.selection.trace('w', self._selection_callback)

        options = [f'Round {n}' for n in range(1, 7)]

        self.dropdown_menu = tk.OptionMenu(master, self.selection, *options)
        self.dropdown_menu.pack()

    def _selection_callback(self, *args):
        round_num = self._round_str_to_int(self.selection.get())
        self.app_ctrl.select_active_round(round_num)

    def _round_str_to_int(self, round_str):
        # round_str must match the regex "Round [1-6]"
        return int(round_str[6])


if __name__ == '__main__':
    App().run()
