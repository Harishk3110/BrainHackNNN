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

## ITERATION 2

Task: AE

Experiment: Add recent-location memory to choose less recently visited legal movement when no collectible is visible.

Hypothesis: The visible-tile policy still defaults to forward-first exploration when no reward tile is visible; a tiny memory should reduce loops and improve reward without affecting visible target pursuit.

Files changed:

- `ae/src/ae_manager.py`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile ae\src\ae_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -c "<target and memory behavior checks>"
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -c "<AE simulation comparison against iteration 1 over seeds 0..4>"
```

Result:

- Target behavior preserved: mission ahead -> `FORWARD`.
- Memory behavior checks:
  - initial no-target state -> `FORWARD`
  - continued no-target state -> `FORWARD` when next forward tile is new
  - masked forward -> `BACKWARD` when legal
- AE simulation comparison with stationary other agents:
  - Seed 0: iteration 1 `55.0`, experiment `84.0`
  - Seed 1: iteration 1 `55.0`, experiment `84.0`
  - Seed 2: iteration 1 `55.0`, experiment `84.0`
  - Seed 3: iteration 1 `55.0`, experiment `84.0`
  - Seed 4: iteration 1 `55.0`, experiment `84.0`

Runtime: local five-seed comparison completed in about 64 seconds.

Decision: kept

Reason: Improves deterministic AE reward, preserves action validity and visible-target behavior, and adds no dependencies.

Next experiment: Add opportunistic bomb placement near visible enemy bases or enemy agents.

## ITERATION 3

Task: AE

Experiment: Opportunistically place bombs when a visible enemy base or enemy agent is aligned within blast radius 2, while skipping obvious allied entities in the same blast line.

Hypothesis: Attack rewards are high, so tightly gated bomb placement near visible enemies could improve reward without slowing inference.

Files changed:

- `ae/src/ae_manager.py`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile ae\src\ae_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -c "<synthetic bomb placement and safety checks>"
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -c "<AE simulation comparison against iteration 2 over seeds 0..4>"
```

Result:

- Synthetic checks:
  - enemy base within blast line -> `PLACE_BOMB`
  - ally in blast line -> skipped bomb and used fallback
  - enemy too far -> skipped bomb
  - no bombs / illegal bomb action -> skipped bomb
- AE simulation comparison with stationary other agents:
  - Seed 0: iteration 2 `84.0`, experiment `84.0`
  - Seed 1: iteration 2 `84.0`, experiment `84.0`
  - Seed 2: iteration 2 `84.0`, experiment `84.0`
  - Seed 3: iteration 2 `84.0`, experiment `84.0`
  - Seed 4: iteration 2 `84.0`, experiment `84.0`

Runtime: local five-seed comparison completed in about 38 seconds after dependencies were available.

Decision: reverted

Reason: No measured reward improvement in the current deterministic validation, so the conservative choice is to avoid extra combat behavior until a scenario shows benefit.

Next experiment: Improve NLP with lightweight lexical retrieval and extractive answers.

## ITERATION 4

Task: NLP

Experiment: Add standard-library lexical retrieval and extractive sentence answers.

Hypothesis: The baseline returns no documents and an empty answer. Ranking documents by lexical overlap and returning the best matching sentence should improve retrieval credit and may improve answer-equivalence credit without adding dependencies.

Files changed:

- `nlp/src/nlp_manager.py`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile nlp\src\nlp_manager.py nlp\src\nlp_server.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -c "<synthetic NLP corpus and QA checks>"
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 --with fastapi==0.115.12 --with 'uvicorn[standard]==0.34.2' python -c "<NLP server import and manager QA check>"
```

Result:

- Empty state: `{'documents': [], 'answer': ''}`.
- Synthetic red-key query: returned `DOC-2` first and answer `The red key is hidden under the garden bench.`
- Synthetic weather query: returned `DOC-3` first and answer `Singapore has humid weather.`
- Server import check: `{'message': 'health ok'}` and valid QA output.

Runtime: all lightweight checks completed in seconds.

Decision: kept

Reason: Clear improvement over empty baseline, preserves official output shape, and adds no dependencies.

Next experiment: Tune NLP scoring to reduce false document matches and improve answer sentence selection.

## ITERATION 5

Task: NLP

Experiment: Suppress zero-score retrieval results.

Hypothesis: Returning arbitrary zero-overlap documents can hurt no-answer cases and pollute top-3 retrieval. If no document has positive lexical overlap, return empty docs and answer; otherwise return only positively scored docs.

Files changed:

- `nlp/src/nlp_manager.py`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile nlp\src\nlp_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -c "<synthetic hit/miss/stopword-only QA checks>"
```

Result:

- Positive query: `{'documents': ['DOC-1'], 'answer': 'The red key is under the garden bench.'}`
- No-match query: `{'documents': [], 'answer': ''}`
- Stopword-only query: `{'documents': [], 'answer': ''}`

Runtime: lightweight checks completed in seconds.

Decision: kept

Reason: Preserves the positive synthetic answer and improves conservative behavior for questions with no lexical evidence.

Next experiment: Improve ASR baseline only if local assets or lightweight dependencies are available; otherwise return to AE.

## ITERATION 6

Task: AE

Experiment: Reduce visible-tile reward multiplier from `10` to `5` so distance matters more when choosing between visible collectibles.

Hypothesis: A closer resource/recon tile may beat a farther mission tile in a short episode, so a lower reward multiplier could improve collection efficiency.

Files changed:

- `ae/src/ae_manager.py`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile ae\src\ae_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -c "<synthetic visible-target check>"
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -c "<AE simulation comparison against HEAD over seeds 0..4>"
```

Result:

- Syntax check passed.
- Synthetic target check returned a legal movement action.
- AE simulation comparison with stationary other agents:
  - Seed 0: current `84.0`, experiment `84.0`
  - Seed 1: current `84.0`, experiment `84.0`
  - Seed 2: current `84.0`, experiment `84.0`
  - Seed 3: current `84.0`, experiment `84.0`
  - Seed 4: current `84.0`, experiment `84.0`

Runtime: local five-seed comparison completed in about 59 seconds after dependencies were available.

Decision: reverted

Reason: No measured gain versus the current AE policy.

Next experiment: Re-check repo state and look for a measurable CV or noising sanity improvement.

## ITERATION 7

Task: AE

Experiment: Add a reusable local AE evaluator script for deterministic seeded policy checks.

Hypothesis: Replacing one-off inline AE simulation commands with a reusable script will improve metric reliability and add invalid-action, repeated-location, and runtime tracking before more policy changes.

Files changed:

- `scripts/eval_ae_local.py`
- `METRICS_REPORT.md`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -m py_compile scripts\eval_ae_local.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
```

Metrics before:

- AE average reward over seeds `0..4`: `84.000`
- Invalid actions: not tracked by reusable script.
- Repeated locations: not tracked by reusable script.

Metrics after:

- Seed rewards: `84.0`, `84.0`, `84.0`, `84.0`, `84.0`
- Average reward: `84.000`
- Average invalid actions: `0.000`
- Average repeated locations: `184.000`

Runtime before: one-off five-seed comparison previously took about `59s` in the slowest logged run.

Runtime after: reusable script total runtime `11.966s`.

Decision: kept

Reason: Metrics are equal for reward, strictly more informative, and faster to run as a repeatable validation command.

Commit: `7b8ba05`

Push status: pushed to `origin/main`

Next: Try one AE policy change that reduces repeated locations without lowering average reward.

## ITERATION 8

Task: AE

Experiment: Turn left/right when both forward and backward movement lead to recently visited locations.

Hypothesis: The current fallback can still shuttle through already visited cells because it prefers movement whenever legal. Turning when both movement options are known repeats should expose a different forward path, reduce repeated locations, and improve reward.

Files changed:

- `ae/src/ae_manager.py`
- `METRICS_REPORT.md`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -m py_compile ae\src\ae_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
```

Metrics before:

- Average reward: `84.000`
- Average invalid actions: `0.000`
- Average repeated locations: `184.000`

Metrics after:

- Seed rewards: `149.0`, `149.0`, `149.0`, `149.0`, `149.0`
- Average reward: `149.000`
- Average invalid actions: `0.000`
- Average repeated locations: `176.000`

Runtime before: `11.966s`

Runtime after: `12.565s`

Decision: kept

Reason: Reward increased by `65.0`, invalid actions stayed at `0`, and repeated locations decreased.

Commit: pending

Push status: pending

Next: Re-run state checks, then try one more AE exploration improvement or move to Docker reporting if Docker is available.

## ITERATION 9

Task: AE

Experiment: Alternate left/right turn preference when both forward and backward lead to recently visited locations.

Hypothesis: Always turning left can create a deterministic loop. Alternating turn direction may expose new paths and improve reward.

Files changed:

- `ae/src/ae_manager.py`
- `METRICS_REPORT.md`
- `TRAINING_RUNS.md`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -m py_compile ae\src\ae_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
```

Metrics before:

- Average reward: `149.000`
- Average invalid actions: `0.000`
- Average repeated locations: `176.000`

Metrics after:

- Seed rewards: `182.0`, `182.0`, `182.0`, `182.0`, `182.0`
- Average reward: `182.000`
- Average invalid actions: `0.000`
- Average repeated locations: `179.000`

Runtime before: `12.565s`

Runtime after: `25.898s`

Decision: kept

Reason: Mixed result, but reward improved by `33.0` with no invalid actions. The slight repeat-count increase is acceptable because score gain is the primary AE metric.

Commit: pending

Push status: pending

Next: Try to preserve the reward gain while reducing repeated locations, or validate Docker if Docker Desktop becomes available.

## ITERATION 10

Task: AE

Experiment: Increase recent-location memory length from `12` to `24`.

Hypothesis: Longer memory may detect longer loops and reduce repeated-location behavior.

Files changed:

- `ae/src/ae_manager.py`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -m py_compile ae\src\ae_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
```

Metrics before:

- Average reward: `182.000`
- Average invalid actions: `0.000`
- Average repeated locations: `179.000`

Metrics after:

- Seed rewards: `182.0`, `182.0`, `182.0`, `182.0`, `182.0`
- Average reward: `182.000`
- Average invalid actions: `0.000`
- Average repeated locations: `180.000`

Runtime before: `25.898s`

Runtime after: `26.072s`

Decision: reverted

Reason: Reward was unchanged and repeated locations worsened slightly.

Commit: pending

Push status: pending

Next: Re-check Docker availability; if still blocked, continue with one AE policy experiment.

## ITERATION 11

Task: AE

Experiment: Add `--opponents stay|random` to the local AE evaluator and seed random opponent action spaces.

Hypothesis: The previous local evaluator used stationary opponents, while the official evaluator samples random actions for other agents. Adding a seeded random-opponent mode gives a more realistic and repeatable validation metric before further policy changes.

Files changed:

- `scripts/eval_ae_local.py`
- `METRICS_REPORT.md`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -m py_compile scripts\eval_ae_local.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents stay
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents random
```

Metrics before:

- Stay-opponent average reward: `182.000`
- Random-opponent metric: not available in reusable evaluator.

Metrics after:

- Stay-opponent average reward: `182.000`
- Stay-opponent invalid actions: `0.000`
- Stay-opponent repeated locations: `179.000`
- Seeded-random-opponent seed rewards: `16.0`, `46.0`, `182.0`, `112.0`, `51.0`
- Seeded-random-opponent average reward: `81.400`
- Seeded-random-opponent invalid actions: `0.000`
- Seeded-random-opponent repeated locations: `168.000`

Runtime before: `25.898s` for stay-opponent run.

Runtime after: `25.016s` for stay-opponent run; `29.520s` for seeded-random-opponent run.

Decision: kept

Reason: Adds a more official-like deterministic metric without changing task policy behavior.

Commit: pending

Push status: pending

Next: Optimize AE against seeded random opponents while preserving stay-opponent score.

## ITERATION 12

Task: AE

Experiment: Avoid visible imminent enemy bomb blast lines before reward targeting.

Hypothesis: Random opponents can place bombs; avoiding visible enemy bombs with low timer may improve random-opponent reward without affecting stationary-opponent score.

Files changed:

- `ae/src/ae_manager.py`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -m py_compile ae\src\ae_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents random
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents stay
```

Metrics before:

- Seeded-random-opponent average reward: `81.400`
- Seeded-random-opponent invalid actions: `0.000`
- Stay-opponent average reward: `182.000`

Metrics after:

- Seeded-random-opponent average reward: `81.400`
- Seeded-random-opponent invalid actions: `0.000`
- Stay-opponent average reward: `182.000`

Runtime before: random `29.520s`; stay `25.016s`

Runtime after: random `31.558s`; stay `27.590s`

Decision: reverted

Reason: Metrics were unchanged and runtime increased slightly.

Commit: pending

Push status: pending

Next: Continue AE random-opponent optimization with one different policy change.

## ITERATION 13

Task: AE

Experiment: Reduce visible-target score multiplier from `10` to `5` under the alternating-turn policy.

Hypothesis: Favoring closer collectibles may improve seeded-random-opponent reward.

Files changed:

- `ae/src/ae_manager.py`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -m py_compile ae\src\ae_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents random
```

Metrics before:

- Seeded-random-opponent average reward: `81.400`
- Seeded-random-opponent invalid actions: `0.000`
- Seeded-random-opponent repeated locations: `168.000`

Metrics after:

- Seeded-random-opponent average reward: `81.400`
- Seeded-random-opponent invalid actions: `0.000`
- Seeded-random-opponent repeated locations: `168.000`

Runtime before: `29.520s`

Runtime after: `26.549s`

Decision: reverted

Reason: No metric improvement.

Commit: pending

Push status: pending

Next: Continue with a different AE policy experiment or wait for dataset paths for ASR/CV/NLP official evaluation.

## DOCKER VALIDATION - AE

Task: AE

Action: Build and smoke test `brainhacknnn-ae`.

Commands run:

```powershell
docker build -t brainhacknnn-ae .
docker run -d --rm -p 5005:5005 --name brainhacknnn-ae-smoke brainhacknnn-ae
Invoke-RestMethod -Uri http://localhost:5005/health
Invoke-RestMethod -Method Post -Uri http://localhost:5005/ae -ContentType 'application/json' -Body <minimal observation JSON>
docker logs brainhacknnn-ae-smoke --tail 50
docker stop brainhacknnn-ae-smoke
```

Result:

- Build passed.
- `/health` returned `health ok`.
- `POST /ae` returned action `4` for a mask where only `STAY` was legal.
- Logs showed HTTP 200 for both smoke requests.

Runtime: build about `22s`; smoke requests completed in seconds.

Decision: kept

Reason: AE Docker image is buildable and the official server interface responds correctly.

Commit: pending

Push status: pending

Next: Docker validation for NLP.

## DOCKER VALIDATION - NLP

Task: NLP

Action: Build and smoke test `brainhacknnn-nlp`.

Commands run:

```powershell
docker build -t brainhacknnn-nlp .
docker run -d --rm -p 5004:5004 --name brainhacknnn-nlp-smoke brainhacknnn-nlp
Invoke-RestMethod -Uri http://localhost:5004/health
Invoke-RestMethod -Method Post -Uri http://localhost:5004/nlp -ContentType 'application/json' -Body <tiny corpus JSON>
Invoke-RestMethod -Method Post -Uri http://localhost:5004/nlp -ContentType 'application/json' -Body <poll JSON>
Invoke-RestMethod -Method Post -Uri http://localhost:5004/nlp -ContentType 'application/json' -Body <question JSON>
docker logs brainhacknnn-nlp-smoke --tail 80
docker stop brainhacknnn-nlp-smoke
```

Result:

- Build passed.
- `/health` returned `health ok`.
- Corpus load request returned `loading`; poll returned `loaded`.
- QA returned document `DOC-1` and answer `Mars is red.`
- Logs showed HTTP 200 for all smoke requests.

Runtime: first NLP build took about `9m` because the large NVIDIA PyTorch base image had to be pulled; smoke requests completed in seconds.

Decision: kept

Reason: NLP Docker image is buildable and the official server interface responds correctly.

Commit: pending

Push status: pending

Next: Docker validation for Noise.

## DOCKER VALIDATION - Noise

Task: Noise

Action: Build and smoke test `brainhacknnn-noise`.

Commands run:

```powershell
docker build -t brainhacknnn-noise .
docker run -d --rm -p 5003:5003 --name brainhacknnn-noise-smoke brainhacknnn-noise
Invoke-RestMethod -Uri http://localhost:5003/health
Invoke-RestMethod -Method Post -Uri http://localhost:5003/noise -ContentType 'application/json' -Body <tiny JPEG JSON>
docker logs brainhacknnn-noise-smoke --tail 80
docker stop brainhacknnn-noise-smoke
```

Result:

- Build passed.
- `/health` returned `health ok`.
- `POST /noise` returned one base64-encoded JPEG prediction.
- Logs showed HTTP 200 for both smoke requests.

Runtime: build completed using cached base layers; smoke requests completed in seconds.

Decision: kept

Reason: Noise Docker image is buildable and the official server interface responds correctly.

Commit: pending

Push status: pending

Next: Docker validation for CV.

## DOCKER VALIDATION - CV

Task: CV

Action: Build and smoke test `brainhacknnn-cv`.

Commands run:

```powershell
docker build -t brainhacknnn-cv .
docker run -d --rm -p 5002:5002 --name brainhacknnn-cv-smoke brainhacknnn-cv
Invoke-RestMethod -Uri http://localhost:5002/health
Invoke-RestMethod -Method Post -Uri http://localhost:5002/cv -ContentType 'application/json' -Body <tiny JPEG JSON>
docker logs brainhacknnn-cv-smoke --tail 80
docker stop brainhacknnn-cv-smoke
```

Result:

- Build passed.
- `/health` returned `health ok`.
- `POST /cv` returned `{"predictions": [[]]}` for one tiny image.
- Logs showed HTTP 200 for both smoke requests.

Runtime: build completed in about `12s`; smoke requests completed in seconds.

Decision: kept

Reason: CV Docker image is buildable and the official server interface responds correctly. The model behavior is still the weak empty-detector baseline.

Commit: pending

Push status: pending

Next: Docker validation for ASR.

## DOCKER VALIDATION - ASR

Task: ASR

Action: Build and smoke test `brainhacknnn-asr`.

Commands run:

```powershell
docker build -t brainhacknnn-asr .
docker run -d --rm -p 5001:5001 --name brainhacknnn-asr-smoke brainhacknnn-asr
Invoke-RestMethod -Uri http://localhost:5001/health
Invoke-RestMethod -Method Post -Uri http://localhost:5001/asr -ContentType 'application/json' -Body <tiny WAV JSON>
docker logs brainhacknnn-asr-smoke --tail 80
docker stop brainhacknnn-asr-smoke
```

Result:

- Build passed.
- `/health` returned `health ok`.
- `POST /asr` returned `{"predictions": [""]}` for one short silent WAV.
- Logs showed HTTP 200 for both smoke requests.

Runtime: build completed in about `15s`; smoke requests completed in seconds.

Decision: kept

Reason: ASR Docker image is buildable and the official server interface responds correctly. The model behavior is still the weak empty-transcript baseline.

Commit: pending

Push status: pending

Next: Confirm data availability and then resume prioritized AE improvements.

## ITERATION 14

Task: AE

Experiment: Prefer an alternating side turn when forward and backward have equal recency during no-target exploration.

Hypothesis: The current fallback defaults to forward on exact recency ties, which can reinforce corridor loops. Turning on ties might expose new paths and reduce repeats without adding dependencies.

Files changed: `ae/src/ae_manager.py` during the trial; reverted after validation.

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents random
```

Metrics before:

- Stay opponents: average reward `182.000`, invalid actions `0.000`, repeated locations `179.000`, runtime `21.869s`.
- Random opponents: average reward `81.400`, invalid actions `0.000`, repeated locations `168.000`, runtime `27.502s`.

Metrics after:

- Stay opponents: average reward `84.000`, invalid actions `0.000`, repeated locations `184.000`, runtime `9.327s`.
- Random opponents: average reward `38.600`, invalid actions `0.000`, repeated locations `165.200`, runtime `14.656s`.

Decision: reverted

Reason: Reward dropped substantially on both validation modes. The small random-opponent repeat reduction did not justify the score loss.

Commit: none

Push status: not needed

Next: Try a narrower AE policy change that preserves the current stay-opponent path while targeting random-opponent robustness.

## ITERATION 15

Task: AE

Experiment: Correct the target-selection viewcone center row from fixed `2` to `len(viewcone) // 2`.

Hypothesis: The README describes `agent_viewcone` as `7 x 5` and centered on the agent, so row `3` might be the correct center for steering toward visible reward tiles.

Files changed: `ae/src/ae_manager.py` during the trial; reverted after validation.

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents random
```

Metrics before:

- Stay opponents: average reward `182.000`, invalid actions `0.000`, repeated locations `179.000`, runtime `21.869s`.
- Random opponents: average reward `81.400`, invalid actions `0.000`, repeated locations `168.000`, runtime `27.502s`.

Metrics after:

- Stay opponents: average reward `0.000`, invalid actions `0.000`, repeated locations `198.000`, runtime `20.763s`.
- Random opponents: average reward `-119.200`, invalid actions `0.000`, repeated locations `197.400`, runtime `25.997s`.

Decision: reverted

Reason: Reward collapsed on both validation modes. The environment's oriented view appears to align with the existing row offset used by the current heuristic.

Commit: none

Push status: not needed

Next: Inspect AE observations/evaluator behavior before another policy edit; prioritize changes that do not disturb current visible-target steering.

## ITERATION 16

Task: AE

Experiment: Ignore visible-target move actions when that move immediately returns to a recently visited cell.

Hypothesis: The current policy can get stuck chasing visible reward channels on cells it just visited. Skipping target-driven forward/backward moves into recent cells should break short loops while preserving legal target steering and side-turn decisions.

Files changed:

- `ae/src/ae_manager.py`
- `METRICS_REPORT.md`
- `DOCKER_REPORT.md`
- `EXPERIMENT_LOG.md`

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents random
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 5 6 7 8 9
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 5 6 7 8 9 --opponents random
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 python -m py_compile ae\src\ae_manager.py
docker build -t brainhacknnn-ae .
docker run -d --rm -p 5005:5005 --name brainhacknnn-ae-smoke brainhacknnn-ae
Invoke-RestMethod -Uri http://localhost:5005/health
Invoke-RestMethod -Method Post -Uri http://localhost:5005/ae -ContentType 'application/json' -Body <minimal observation JSON>
docker logs brainhacknnn-ae-smoke --tail 60
docker stop brainhacknnn-ae-smoke
```

Metrics before:

- Stay opponents seeds `0..4`: average reward `182.000`, invalid actions `0.000`, repeated locations `179.000`, runtime `21.869s`.
- Random opponents seeds `0..4`: average reward `81.400`, invalid actions `0.000`, repeated locations `168.000`, runtime `27.502s`.

Metrics after:

- Stay opponents seeds `0..4`: average reward `195.000`, invalid actions `0.000`, repeated locations `177.000`, runtime `15.673s`.
- Random opponents seeds `0..4`: average reward `154.200`, invalid actions `0.000`, repeated locations `159.400`, runtime `22.198s`.
- Stay opponents seeds `0..9`: average reward `195.000`, invalid actions `0.000`, repeated locations `177.000`, runtime `31.366s`.
- Random opponents seeds `0..9`: average reward `164.800`, invalid actions `0.000`, repeated locations `156.100`, runtime `40.408s`.
- AE Docker rebuild and route smoke test: passed.

Runtime before:

- Stay opponents seeds `0..4`: `21.869s`
- Random opponents seeds `0..4`: `27.502s`

Runtime after:

- Stay opponents seeds `0..4`: `15.673s`
- Random opponents seeds `0..4`: `22.198s`

Decision: kept

Reason: Improved measured AE reward in both validation modes, reduced repeated locations, preserved zero invalid actions, and passed Docker smoke validation.

Commit: `c748392 experiment(ae): avoid recently visited target moves`

Push status: pushed to `origin/main`

Next: Re-check clean state, then choose one more AE experiment unless a dataset path appears for ASR/CV/NLP.

## ITERATION 17

Task: AE

Experiment: Increase recent-location memory from `12` to `20`.

Hypothesis: With the recent-target guard in place, a longer memory may avoid revisiting stale reward-looking cells and reduce loops further.

Files changed: `ae/src/ae_manager.py` during the trial; reverted after validation.

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents random
```

Metrics before:

- Stay opponents: average reward `195.000`, invalid actions `0.000`, repeated locations `177.000`.
- Random opponents: average reward `154.200`, invalid actions `0.000`, repeated locations `159.400`.

Metrics after:

- Stay opponents: average reward `161.000`, invalid actions `0.000`, repeated locations `177.000`, runtime `8.205s`.
- Random opponents: average reward `84.400`, invalid actions `0.000`, repeated locations `154.600`, runtime `10.465s`.

Decision: reverted

Reason: Reward dropped substantially in both modes. The small random-opponent repeat reduction did not justify the score loss.

Commit: none

Push status: not needed

Next: Try a narrower AE change; preserve `RECENT_LIMIT = 12`.

## ITERATION 18

Task: AE

Experiment: Break no-target spin loops after repeatedly staying on the same cell.

Hypothesis: When no target is visible, the policy sometimes spends many controlled turns rotating on one cell. Tracking a same-location streak and forcing movement after several turns might improve exploration.

Files changed: `ae/src/ae_manager.py` during the trial; reverted after validation.

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents random
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 5 6 7 8 9
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 5 6 7 8 9 --opponents random
Get-Content test\test_ae.py
```

Metrics before:

- Stay opponents seeds `0..4`: average reward `195.000`, invalid actions `0.000`, repeated locations `177.000`.
- Random opponents seeds `0..4`: average reward `154.200`, invalid actions `0.000`, repeated locations `159.400`.
- Random opponents seeds `0..9`: average reward `164.800`, invalid actions `0.000`, repeated locations `156.100`.

Metrics after:

- Stay opponents seeds `0..4`: average reward `202.000`, invalid actions `0.000`, repeated locations `177.000`, runtime `7.230s`.
- Random opponents seeds `0..4`: average reward `149.200`, invalid actions `0.000`, repeated locations `151.600`, runtime `8.997s`.
- Stay opponents seeds `0..9`: average reward `202.000`, invalid actions `0.000`, repeated locations `177.000`, runtime `23.691s`.
- Random opponents seeds `0..9`: average reward `149.600`, invalid actions `0.000`, repeated locations `146.900`, runtime `32.450s`.

Decision: reverted

Reason: Official `test/test_ae.py` uses random actions for other agents. The random-opponent proxy got worse even though stationary-opponent reward improved.

Commit: none

Push status: not needed

Next: Continue AE experiments against random opponents as the primary proxy.

## AE OFFICIAL-STYLE LOCAL VALIDATION

Task: AE

Action: Run the official local AE evaluator against the current Docker image.

Commands run:

```powershell
docker run -d --rm -p 5005:5005 --name brainhacknnn-ae-official brainhacknnn-ae
$env:TEAM_TRACK='novice'; $env:TEAM_NAME='BrainHackNNN'; $env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae --with requests --with python-dotenv --with tqdm python test\test_ae.py
docker logs brainhacknnn-ae-official --tail 80
docker stop brainhacknnn-ae-official
```

Result:

- Official local evaluator completed.
- Total rewards: `1099.0`.
- Score: `0.18316666666666664`.
- Container logs showed HTTP 200 responses during evaluation.

Decision: recorded

Reason: This is the closest local validation to the official AE scoring path currently available.

Commit: pending

Push status: pending

Next: Continue one-at-a-time AE experiments using random-opponent local metrics as the primary proxy.

## ITERATION 19

Task: AE

Experiment: Increase resource tile priority from `2.0` to `3.0`.

Hypothesis: A slightly higher resource weight may improve collection under random opponents without changing runtime or interfaces.

Files changed: `ae/src/ae_manager.py` during the trial; reverted after validation.

Commands run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4 --opponents random
```

Metrics before:

- Stay opponents: average reward `195.000`, invalid actions `0.000`, repeated locations `177.000`.
- Random opponents: average reward `154.200`, invalid actions `0.000`, repeated locations `159.400`.

Metrics after:

- Stay opponents: average reward `195.000`, invalid actions `0.000`, repeated locations `177.000`, runtime `20.285s`.
- Random opponents: average reward `154.200`, invalid actions `0.000`, repeated locations `159.400`, runtime `26.427s`.

Decision: reverted

Reason: No reward or repeat-count improvement.

Commit: none

Push status: not needed

Next: Continue AE random-opponent experiments; avoid neutral target-weight tweaks unless a diagnostic supports them.
