"""Manages the AE model."""


class AEManager:
    TILE_RECON = 6
    TILE_MISSION = 7
    TILE_RESOURCE = 8

    ACTION_FORWARD = 0
    ACTION_BACKWARD = 1
    ACTION_LEFT = 2
    ACTION_RIGHT = 3
    ACTION_STAY = 4
    ACTION_PLACE_BOMB = 5

    def __init__(self):
        # This is where you can initialize your model and any static configurations.
        # TODO
        pass

    def ae(self, observation: dict[str, int | list[int]]) -> int:
        """Gets the next action for the agent, based on the observation.

        Args:
            observation: The observation from the environment. See
                `ae/README.md` for the format.

        Returns:
            An integer representing the action to take. See `ae/README.md` for
            the options.
        """

        action_mask = observation.get("action_mask", [])
        if not isinstance(action_mask, list):
            action_mask = []

        target_action = self._action_toward_best_visible_tile(observation)
        if self._is_legal(target_action, action_mask):
            return target_action

        for action in (
            self.ACTION_FORWARD,
            self.ACTION_STAY,
            self.ACTION_BACKWARD,
            self.ACTION_LEFT,
            self.ACTION_RIGHT,
            self.ACTION_PLACE_BOMB,
        ):
            if self._is_legal(action, action_mask):
                return action

        return 0

    def _action_toward_best_visible_tile(self, observation: dict) -> int | None:
        viewcone = observation.get("agent_viewcone")
        if not isinstance(viewcone, list) or not viewcone:
            return None

        center_row = min(2, len(viewcone) - 1)
        center_col = min(2, len(viewcone[center_row]) - 1)
        best: tuple[float, int, int] | None = None

        for row_idx, row in enumerate(viewcone):
            if not isinstance(row, list):
                continue
            for col_idx, channels in enumerate(row):
                if not isinstance(channels, list):
                    continue

                reward = self._tile_reward(channels)
                if reward <= 0:
                    continue

                forward_delta = row_idx - center_row
                lateral_delta = col_idx - center_col
                distance = abs(forward_delta) + abs(lateral_delta)
                if distance == 0:
                    continue

                score = reward * 10 - distance
                candidate = (score, forward_delta, lateral_delta)
                if best is None or candidate > best:
                    best = candidate

        if best is None:
            return None

        _, forward_delta, lateral_delta = best
        if forward_delta > 0 and abs(forward_delta) >= abs(lateral_delta):
            return self.ACTION_FORWARD
        if forward_delta < 0 and abs(forward_delta) >= abs(lateral_delta):
            return self.ACTION_BACKWARD
        if lateral_delta < 0:
            return self.ACTION_LEFT
        if lateral_delta > 0:
            return self.ACTION_RIGHT
        return None

    def _tile_reward(self, channels: list) -> float:
        reward = 0.0
        if self._channel_active(channels, self.TILE_MISSION):
            reward = max(reward, 5.0)
        if self._channel_active(channels, self.TILE_RESOURCE):
            reward = max(reward, 2.0)
        if self._channel_active(channels, self.TILE_RECON):
            reward = max(reward, 1.0)
        return reward

    def _channel_active(self, channels: list, index: int) -> bool:
        return index < len(channels) and channels[index] > 0.5

    def _is_legal(self, action: int | None, action_mask: list) -> bool:
        return action is not None and action < len(action_mask) and bool(action_mask[action])
