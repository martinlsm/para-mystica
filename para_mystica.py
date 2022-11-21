import tkinter as tk

from actions import ActionError

from action_buttons import action_button_create
from factions import *
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
        self.app.select_active_round(round_num)

    def append_game_event(self, text, action):
        self.app.append_game_event(text, action)


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Para Mystica')

        FactionSelector(self.root, AppController(self))

        rounds_master = tk.Frame(self.root)
        rounds_master.pack()
        self.round_frames = \
                [RoundFrame(rounds_master, f'Round {col + 1}', 0, col) \
                    for col in range(0, 6)]

        self.active_round_selector = ActiveRoundSelector(AppController(self), self.root)

        self.log = Log(self.root, 5)

        # These attributes is set by various events.
        self.faction_state_tracker = None
        # TODO: Is it good to secretly set this to 1 here?
        self.active_round = 1
        self.action_selector = None

    def run(self):
        self.root.mainloop()

    def select_faction(self, faction_name):
        # TODO: More cleanup is needed here. All round frames need to be refreshed.
        if self.faction_state_tracker is not None:
            self.action_selector.destroy()

        self.faction_state_tracker = FactionStateTracker(faction_name)

        self.action_selector = ActionSelector(self.root, AppController(self),
                                              faction_name)
        self._update_round_displays()

    def append_game_event(self, text, action):
        try:
            self.faction_state_tracker.append_action(action, self.active_round)
        except ActionError as e:
            self.log.error(e)
            return

        round_idx = self.active_round - 1
        self.round_frames[round_idx].push_back_action(text)

        self._update_round_displays()

    def select_active_round(self, round_num):
        self.active_round = round_num

    def _update_round_displays(self):
        # TODO: Enable skipping of updating earlier rounds
        self.faction_state_tracker._update(1)
        resource_list = self.faction_state_tracker.get_resource_lists()

        for (res_before, res_after), round_frame \
                in zip(resource_list, self.round_frames):
            round_frame.update_round_info(res_before, res_after)


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
    def __init__(self, master, app_ctrl, faction_name):
        self.app_ctrl = app_ctrl

        self.frame = tk.Frame(master)
        self.frame.pack()

        self.act_btns = []
        self.grid_width = 5

        for action in supported_actions(faction_name):
            self._add_action_button(action)

    def destroy(self):
        self.frame.destroy()

    def _add_action_button(self, action):
        grid_row = len(self.act_btns) // 5
        grid_col = len(self.act_btns) % self.grid_width

        btn = action_button_create(self.app_ctrl, self.frame, action, grid_row,
                                   grid_col)
        self.act_btns.append(btn)


class ActionSequenceView:
    def __init__(self, master):
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE,
                                  activestyle=tk.NONE)
        self.listbox.pack()

    def push_back(self, text):
        self.listbox.insert(tk.END, text)

    def pop_back(self):
        self.listbox.delete(tk.END)


class RoundFrame:
    def __init__(self, master, label, row, col):
        frame = tk.Frame(master)
        frame.grid(row=row, column=col)

        self.label = tk.Label(frame, text=label)
        self.label.pack()

        self.action_sequence = ActionSequenceView(frame)

        self.round_info_display = RoundInfoDisplay(frame)
        self.round_info_display.update(Resources(), Resources())

    def push_back_action(self, text):
        self.action_sequence.push_back(text)

    def pop_back_action(self):
        self.action_sequence.pop_back()

    def get_actions(self):
        return self.event_sequence.get_actions()

    def update_round_info(self, before_round_res, after_round_res):
        self.round_info_display.update(before_round_res, after_round_res)


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


class Log:
    def __init__(self, master, height):
        # TODO: Set font.
        self.text = tk.Text(master, height=height)
        self.text.pack(expand=True, fill='both', padx=5, pady=5)

        self.line_count = 0

        self.info_tag = 'info'
        self.error_tag = 'error'
        self.warning_tag = 'warning'

        self.text.tag_config(self.info_tag, background='gray', foreground='black')
        self.text.tag_config(self.error_tag, background='red', foreground='black')
        self.text.tag_config(self.warning_tag, background='yellow', foreground='black')

    def info(self, msg):
        self._log('INFO', msg, self.info_tag)

    def error(self, msg):
        self._log('ERROR', msg, self.error_tag)

    def warning(self, msg):
        self._log('WARNING', msg, self.warning_tag)

    def _log(self, prefix, msg, tag):
        self.text.config(state=tk.NORMAL)

        self.line_count += 1

        self.text.insert(tk.END, f'{prefix}: {msg}\n')
        self.text.tag_add(tag, f'{self.line_count}.0', f'{self.line_count}.{len(prefix)}')

        self.text.config(state=tk.DISABLED)



if __name__ == '__main__':
    App().run()
