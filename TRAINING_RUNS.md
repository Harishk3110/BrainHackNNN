# Training Runs

Updated: 2026-05-14

No real training runs have been executed yet.

Reason:

- ASR training data is missing locally.
- CV training data is missing locally.
- NLP official question/document data is missing locally; current NLP system is dependency-light retrieval, not a trained model.
- AE currently uses deterministic heuristic policy iteration with seeded simulation, not RL training.
- Noising does not currently use a trained model.

## Recorded Optimization Runs

### AE Heuristic Evaluation

- Task: AE
- Date/time: 2026-05-14
- Command:
  ```powershell
  $env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
  ```
- Dataset path: not applicable; uses `til-26-ae/til_environment`.
- Hyperparameters:
  - recent memory length: `12`
  - visible target score: `reward * 10 - distance`
  - turn when forward/backward are both recent repeats
- Metric before: average reward `84.000`, repeated locations `184.000`, invalid actions `0.000`
- Metric after: average reward `149.000`, repeated locations `176.000`, invalid actions `0.000`
- Runtime: `12.565s`
- Artifact path: code-only policy in `ae/src/ae_manager.py`
- Decision: kept

### AE Alternating Turn Heuristic

- Task: AE
- Date/time: 2026-05-14
- Command:
  ```powershell
  $env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
  ```
- Dataset path: not applicable; uses `til-26-ae/til_environment`.
- Hyperparameters:
  - recent memory length: `12`
  - turn when forward/backward are both recent repeats
  - alternate repeated-corridor turn preference between left and right
- Metric before: average reward `149.000`, repeated locations `176.000`, invalid actions `0.000`
- Metric after: average reward `182.000`, repeated locations `179.000`, invalid actions `0.000`
- Runtime: `25.898s`
- Artifact path: code-only policy in `ae/src/ae_manager.py`
- Decision: kept; reward gain outweighed small repeat-count regression.
