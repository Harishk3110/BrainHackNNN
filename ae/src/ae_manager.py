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
    RECENT_LIMIT = 12

    def __init__(self):
        # This is where you can initialize your model and any static configurations.
        # TODO
        self.recent_locations: list[tuple[int, int]] = []

    def ae(self, observation: dict[str, int | list[int]]) -> int:
        """Gets the next action for the agent, based on the observation.

        Args:
            observation: The observation from the environment. See
                `ae/README.md` for the format.

        Returns:
            An integer representing the action to take. See `ae/README.md` for
            the options.
        """

        if observation.get("step") == 0:
            self.recent_locations = []

        self._remember_location(observation.get("location"))

        action_mask = observation.get("action_mask", [])
        if not isinstance(action_mask, list):
            action_mask = []

        target_action = self._action_toward_best_visible_tile(observation)
        if self._is_legal(target_action, action_mask):
            return target_action

        explore_action = self._least_recent_move(observation, action_mask)
        if self._is_legal(explore_action, action_mask):
            return explore_action

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

    def _remember_location(self, location: object) -> None:
        if not isinstance(location, list) or len(location) < 2:
            return
        current = (int(location[0]), int(location[1]))
        self.recent_locations.append(current)
        if len(self.recent_locations) > self.RECENT_LIMIT:
            self.recent_locations = self.recent_locations[-self.RECENT_LIMIT:]

    def _least_recent_move(self, observation: dict, action_mask: list) -> int | None:
        location = observation.get("location")
        direction = observation.get("direction")
        if not isinstance(location, list) or len(location) < 2 or not isinstance(direction, int):
            return None

        current = (int(location[0]), int(location[1]))
        candidates = []
        for action in (self.ACTION_FORWARD, self.ACTION_BACKWARD):
            if not self._is_legal(action, action_mask):
                continue
            next_location = self._next_location(current, direction, action)
            recency = self._location_recency(next_location)
            candidates.append((0 if recency == 0 else 1, -recency, action))

        if candidates and all(candidate[0] == 1 for candidate in candidates):
            for action in (self.ACTION_LEFT, self.ACTION_RIGHT):
                if self._is_legal(action, action_mask):
                    return action

        if candidates:
            candidates.sort()
            return candidates[0][2]

        for action in (self.ACTION_LEFT, self.ACTION_RIGHT, self.ACTION_STAY):
            if self._is_legal(action, action_mask):
                return action
        return None

    def _next_location(self, location: tuple[int, int], direction: int, action: int) -> tuple[int, int]:
        dx, dy = self._direction_delta(direction)
        if action == self.ACTION_BACKWARD:
            dx, dy = -dx, -dy
        return location[0] + dx, location[1] + dy

    def _direction_delta(self, direction: int) -> tuple[int, int]:
        match direction:
            case 0:
                return 1, 0
            case 1:
                return 0, 1
            case 2:
                return -1, 0
            case 3:
                return 0, -1
            case _:
                return 0, 0

    def _location_recency(self, location: tuple[int, int]) -> int:
        for index in range(len(self.recent_locations) - 1, -1, -1):
            if self.recent_locations[index] == location:
                return len(self.recent_locations) - index
        return 0
