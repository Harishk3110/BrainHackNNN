# Experiment Log

Created: 2026-05-14

## Baseline Setup

Commands run:

```powershell
git status --short --branch
git remote -v
git submodule status
Get-Command til
Get-Command docker
Get-Command python
Get-Command py
Get-Command python3
Get-Command conda
Get-Command uv
docker info
$env:UV_CACHE_DIR='.uv-cache'; uv python list
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile asr\src\asr_manager.py asr\src\asr_server.py cv\src\cv_manager.py cv\src\cv_server.py noise\src\noise_manager.py noise\src\noise_server.py nlp\src\nlp_manager.py nlp\src\nlp_server.py ae\src\ae_manager.py ae\src\ae_server.py test\test_asr.py test\test_cv.py test\test_noise.py test\test_nlp.py test\test_ae.py
til test asr
til test cv
til test noise
til test nlp
til test ae
```

Findings:

- Repo root is `til-26/` inside the VS Code workspace.
- Working branch starts at `main...origin/main`.
- `origin` is `https://github.com/Harishk3110/Harishk3110.git`.
- `upstream` is `https://github.com/til-ai/til-26.git`.
- Submodules are configured but not initialized locally.
- `til`, global `python`, `py`, `python3`, `pip`, `conda`, and `pytest` are unavailable on PATH.
- `uv` and Docker CLI are available.
- Docker daemon is not usable here because Docker Desktop cannot start.
- Official data paths under `/home/jupyter/...` are not present in this Windows workspace.

Baseline fixes made:

- `noise/src/noise_manager.py`: save the PIL image directly as JPEG instead of calling `Image.fromarray()` on a PIL image.
- `ae/src/ae_manager.py`: return a legal action from `action_mask` instead of always returning `FORWARD`.

Baseline validation:

- Syntax compile: passed.
- ASR lightweight check: health/import passed; returns empty transcript.
- CV lightweight check: health/import passed; returns empty detections.
- Noise lightweight check: passed with valid base64 JPEG output.
- NLP lightweight check: health/import/load flag passed; returns empty answer and no documents.
- AE lightweight check: passed checked action masks and returns legal fallback actions.

No scored official baseline is available locally until `til`, Docker, submodules, environment variables, and `/home/jupyter/{TEAM_TRACK}` data are available.

## ITERATION 1

Task: AE

Experiment: Steer toward visible mission/resource/recon tiles in `agent_viewcone`.

Hypothesis: The always-forward baseline misses visible reward tiles; a deterministic policy that moves or turns toward the best visible collectible should improve AE reward without adding dependencies or slowing inference.

Files changed:

- `ae/src/ae_manager.py`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile ae\src\ae_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -c "<synthetic viewcone checks>"
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -c "<AE simulation comparison over seeds 0,1,2>"
```

Result:

- Synthetic checks:
  - mission ahead -> `FORWARD`
  - resource left -> `LEFT`
  - recon right -> `RIGHT`
  - mission behind -> `BACKWARD`
  - masked preferred forward -> legal fallback `STAY`
- AE simulation comparison with stationary other agents:
  - Seed 0: baseline `0.0`, experiment `55.0`
  - Seed 1: baseline `0.0`, experiment `55.0`
  - Seed 2: baseline `0.0`, experiment `55.0`

Runtime: local three-seed comparison completed in about 23 seconds after dependencies were cached.

Decision: kept

Reason: Improves simulated AE reward versus baseline on deterministic seeds, preserves interface, adds no dependencies, and remains fast.

Next experiment: Add AE anti-loop exploration memory for cases with no visible collectible target.
