from factions import create_faction, next_round, process_actions, resolve_action

class FactionStateTracker:
    def __init__(self, faction_name):
        self.faction_name = faction_name

        # TODO: Make a class for this.
        self.action_lists = [[] for _ in range(6)]
        self.pre_game_state = create_faction(faction_name)
        self.pre_round_states = [None for _ in range(6)]
        self.post_round_states = [None for _ in range(6)]

        self._update(1)

    def get_resource_lists(self):
        return ((pre.get_resources(), post.get_resources()) \
                for (pre, post) \
                in zip(self.pre_round_states, self.post_round_states))

    def append_action(self, action, round):
        # TODO: This is not complete. There is a bug when updating a round and
        # later rounds have actions in them.
        round_idx = round - 1

        # Create a copy of a faction and test the action with it.
        # If the action fails, resolve_action() will throw an exception.
        temp_faction_state = self.post_round_states[round_idx].copy()
        resolve_action(temp_faction_state, action)

        # Update the actual faction state and append the action to the
        # corresponding list.
        self.post_round_states[round_idx] = temp_faction_state
        self.action_lists[round_idx].append(action)

        # Update following rounds since they are affected by the new action.
        self._update(round + 1)

    def _update(self, from_round):
        assert 1 <= from_round

        for rnd in range(from_round, 7):
            rnd_idx = rnd - 1
            self.pre_round_states[rnd_idx] = \
                    next_round(self._get_post_round_state(rnd - 1))
            self.post_round_states[rnd_idx] = \
                    process_actions(self.pre_round_states[rnd_idx],
                                    self.action_lists[rnd_idx])

    def _get_post_round_state(self, round):
        if round == 0:
            return self.pre_game_state
        return self.post_round_states[round - 1]
