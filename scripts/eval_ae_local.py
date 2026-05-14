"""Local AE heuristic evaluator.

Runs the current AEManager directly inside til_environment without starting a
FastAPI server. This is a lightweight sanity metric, not a replacement for the
official `til test ae` command.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ae" / "src"))

from ae_manager import AEManager  # noqa: E402
from til_environment import bomberman_env  # noqa: E402
from til_environment.config import default_config  # noqa: E402


def to_jsonable_observation(observation: dict) -> dict:
    return {
        key: value if type(value) in (int, float) else value.tolist()
        for key, value in observation.items()
    }


def run_seed(seed: int, max_agent_steps: int | None = None) -> dict[str, float | int]:
    cfg = default_config()
    cfg.env.novice = True
    cfg.env.render_mode = None
    env = bomberman_env.basic_env(env_wrappers=[], cfg=cfg)
    env.reset(seed=seed)

    controlled_agent = env.possible_agents[0]
    manager = AEManager()
    rewards = {agent: 0.0 for agent in env.possible_agents}
    invalid_actions = 0
    repeated_locations = 0
    seen_locations: set[tuple[int, int]] = set()
    agent_steps = 0

    started_at = time.perf_counter()
    for current_agent in env.agent_iter():
        observation, _reward, termination, truncation, _info = env.last()
        for agent in env.agents:
            rewards[agent] += env.rewards[agent]

        if termination or truncation:
            action = None
        elif current_agent == controlled_agent:
            jsonable_observation = to_jsonable_observation(observation)
            location = jsonable_observation.get("location")
            if isinstance(location, list) and len(location) >= 2:
                location_tuple = (int(location[0]), int(location[1]))
                if location_tuple in seen_locations:
                    repeated_locations += 1
                seen_locations.add(location_tuple)

            action = int(manager.ae(jsonable_observation))
            action_mask = jsonable_observation.get("action_mask", [])
            if not (
                isinstance(action_mask, list)
                and action < len(action_mask)
                and bool(action_mask[action])
            ):
                invalid_actions += 1

            agent_steps += 1
            if max_agent_steps is not None and agent_steps >= max_agent_steps:
                env.step(action)
                break
        else:
            action = 4 if observation["action_mask"][4] else None

        env.step(action)

    runtime = time.perf_counter() - started_at
    env.close()

    return {
        "seed": seed,
        "reward": rewards[controlled_agent],
        "invalid_actions": invalid_actions,
        "repeated_locations": repeated_locations,
        "runtime_sec": runtime,
        "agent_steps": agent_steps,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2, 3, 4])
    parser.add_argument("--max-agent-steps", type=int, default=None)
    args = parser.parse_args()

    results = [run_seed(seed, args.max_agent_steps) for seed in args.seeds]
    avg_reward = sum(float(result["reward"]) for result in results) / len(results)
    avg_invalid = sum(int(result["invalid_actions"]) for result in results) / len(results)
    avg_repeats = sum(int(result["repeated_locations"]) for result in results) / len(results)
    total_runtime = sum(float(result["runtime_sec"]) for result in results)

    for result in results:
        print(
            "seed={seed} reward={reward:.1f} invalid={invalid_actions} "
            "repeats={repeated_locations} steps={agent_steps} runtime={runtime_sec:.3f}s".format(
                **result
            )
        )
    print(f"avg_reward={avg_reward:.3f}")
    print(f"avg_invalid_actions={avg_invalid:.3f}")
    print(f"avg_repeated_locations={avg_repeats:.3f}")
    print(f"total_runtime_sec={total_runtime:.3f}")


if __name__ == "__main__":
    main()
