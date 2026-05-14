# Baseline Plan

Created: 2026-05-14

## Repository Map

- `README.md`: official setup, build, test, and submit overview.
- `requirements-dev.txt`: local evaluator/test dependencies.
- `asr/`: automatic speech recognition task.
  - `asr/src/asr_server.py`: FastAPI server, route `POST /asr`, port `5001`.
  - `asr/src/asr_manager.py`: ASR inference implementation point.
  - `asr/Dockerfile`: ASR container build.
  - `asr/requirements.txt`: ASR container dependencies.
- `cv/`: object detection task.
  - `cv/src/cv_server.py`: FastAPI server, route `POST /cv`, port `5002`.
  - `cv/src/cv_manager.py`: CV inference implementation point.
  - `cv/Dockerfile`: CV container build.
  - `cv/requirements.txt`: CV container dependencies.
- `noise/`: adversarial noising task for CV inputs.
  - `noise/src/noise_server.py`: FastAPI server, route `POST /noise`, port `5003`.
  - `noise/src/noise_manager.py`: noising implementation point.
  - `noise/Dockerfile`: Noise container build.
  - `noise/requirements.txt`: Noise container dependencies.
- `nlp/`: RAG question-answering task.
  - `nlp/src/nlp_server.py`: FastAPI server, route `POST /nlp`, port `5004`.
  - `nlp/src/nlp_manager.py`: corpus loading and QA implementation point.
  - `nlp/Dockerfile`: NLP container build.
  - `nlp/requirements.txt`: NLP container dependencies.
- `ae/`: autonomous exploration task.
  - `ae/src/ae_server.py`: FastAPI server, route `POST /ae`, port `5005`.
  - `ae/src/ae_manager.py`: action policy implementation point.
  - `ae/Dockerfile`: AE container build.
  - `ae/requirements.txt`: AE container dependencies.
- `test/`: official local test/evaluation scripts used by `til test`.
  - `test/test_asr.py`: ASR evaluator, reads `/home/jupyter/{TEAM_TRACK}/asr`.
  - `test/test_cv.py`: CV evaluator, reads `/home/jupyter/{TEAM_TRACK}/cv`.
  - `test/test_noise.py`: Noise evaluator, reads `/home/jupyter/{TEAM_TRACK}/cv`.
  - `test/test_nlp.py`: NLP evaluator, reads `/home/jupyter/{TEAM_TRACK}/nlp`.
  - `test/test_ae.py`: AE evaluator using `til_environment`.
  - `test/noise_eval/`: image distortion/fairness checks for noising.
- `til-26-ae/`: git submodule for `til_environment`; currently empty locally.
- `til-26-finals/`: git submodule for later competition phases; currently empty locally.

## Git Remotes

- `origin`: `https://github.com/Harishk3110/Harishk3110.git`
- `upstream`: `https://github.com/til-ai/til-26.git`

## Current Baseline Behavior

- ASR: `ASRManager.asr()` returns `""`.
- CV: `CVManager.cv()` returns `[]`.
- Noise: `NoiseManager.noise()` attempts `Image.fromarray(img)` where `img` is a PIL image, catches exceptions, and returns the original image as base64.
- NLP: `NLPManager.load_corpus()` sets `loaded = True`; `qa()` returns `{"documents": [], "answer": ""}`.
- AE: `AEManager.ae()` always returns action `0` (`FORWARD`) without checking `action_mask`.

## Install Commands

Official local/dev install:

```bash
git submodule update --init
pip install -r requirements-dev.txt
```

Per-task container dependencies are installed by each Dockerfile from that task's `requirements.txt`.

Local direct installs, if testing without Docker:

```bash
pip install -r asr/requirements.txt
pip install -r cv/requirements.txt
pip install -r noise/requirements.txt
pip install -r nlp/requirements.txt
pip install -r ae/requirements.txt
```

## Run Commands

Run each service locally from its task `src/` directory:

```bash
cd asr/src && uvicorn asr_server:app --port 5001 --host 0.0.0.0
cd cv/src && uvicorn cv_server:app --port 5002 --host 0.0.0.0
cd noise/src && uvicorn noise_server:app --port 5003 --host 0.0.0.0
cd nlp/src && uvicorn nlp_server:app --port 5004 --host 0.0.0.0
cd ae/src && uvicorn ae_server:app --port 5005 --host 0.0.0.0
```

## Test / Evaluation Commands

Official wrapper commands on GCP Workbench:

```bash
til test asr
til test cv
til test noise
til test nlp
til test ae
```

Direct evaluator scripts, assuming the matching service is running and `TEAM_NAME`, `TEAM_TRACK`, `/home/jupyter/{TEAM_TRACK}`, and dependencies are available:

```bash
python test/test_asr.py
python test/test_cv.py
python test/test_noise.py
python test/test_nlp.py
python test/test_ae.py
```

Expected evaluator data paths:

- ASR: `/home/jupyter/{TEAM_TRACK}/asr/asr.jsonl` and referenced WAV files.
- CV: `/home/jupyter/{TEAM_TRACK}/cv/annotations.json` and `/home/jupyter/{TEAM_TRACK}/cv/images`.
- Noise: same CV data path as CV.
- NLP: `/home/jupyter/{TEAM_TRACK}/nlp/nlp.jsonl`, `/home/jupyter/{TEAM_TRACK}/nlp/documents`, and possibly `/home/jupyter/{TEAM_TRACK}/nlp/models`.
- AE: installed `til_environment` from `til-26-ae` submodule.

## Docker Build Commands

Official wrapper:

```bash
til build asr
til build cv
til build noise
til build nlp
til build ae
```

Manual Docker build equivalents:

```bash
cd asr && docker build -t TEAM_ID-asr:latest .
cd cv && docker build -t TEAM_ID-cv:latest .
cd noise && docker build -t TEAM_ID-noise:latest .
cd nlp && docker build -t TEAM_ID-nlp:latest .
cd ae && docker build -t TEAM_ID-ae:latest .
```

## Submission Commands

Official wrapper:

```bash
til submit asr
til submit cv
til submit noise
til submit nlp
til submit ae
```

## Known Missing Data / Dependencies In This Local Workspace

- `python`, `py`, and `pip` are not available on PATH in this VS Code terminal environment.
- `TEAM_NAME` and `TEAM_TRACK` are not set.
- `/home/jupyter/...` competition data paths do not exist in this Windows workspace.
- `til-26-ae/` and `til-26-finals/` submodule directories are empty; `git submodule status` shows both are not initialized.
- The official `til` CLI is not confirmed available locally.
- Docker availability has not yet been validated.
- Because Python is unavailable on PATH, local service startup and evaluator scripts cannot yet run in this environment.

## First Baseline Checklist

1. Initialize submodules:
   ```bash
   git submodule update --init
   ```
2. Make Python 3.10+ and `pip` available on PATH, or run inside the GCP Workbench environment.
3. Install dev dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Set environment:
   ```bash
   TEAM_NAME=<team-name>
   TEAM_TRACK=<novice-or-advanced>
   ```
5. Confirm expected data exists under `/home/jupyter/{TEAM_TRACK}`.
6. Start each task service and run the corresponding evaluator.
7. Record command, output, failure, fix, rerun, and final status for ASR, CV, Noise, NLP, and AE.
8. Keep Docker compatibility by testing task builds after any dependency or entrypoint change.

## Baseline Validation Status

Local environment constraints:

- `til test <task>` cannot run locally because `til` is not installed on PATH.
- Docker builds cannot run locally because Docker Desktop reports: `Docker Desktop is unable to start`.
- Full official evaluators cannot run here because `/home/jupyter/{TEAM_TRACK}` data paths are absent and `TEAM_NAME` / `TEAM_TRACK` are unset.
- `uv` was used with repo-local cache via `$env:UV_CACHE_DIR='.uv-cache'` to run Python 3.14 checks.

Syntax validation:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile asr\src\asr_manager.py asr\src\asr_server.py cv\src\cv_manager.py cv\src\cv_server.py noise\src\noise_manager.py noise\src\noise_server.py nlp\src\nlp_manager.py nlp\src\nlp_server.py ae\src\ae_manager.py ae\src\ae_server.py test\test_asr.py test\test_cv.py test\test_noise.py test\test_nlp.py test\test_ae.py
```

Result: passed.

Task checks:

- ASR
  - Command:
    ```powershell
    $env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 --with fastapi==0.115.12 --with 'uvicorn[standard]==0.34.2' python -c "import sys; sys.path.insert(0, 'asr/src'); import asr_server; print(asr_server.health()); print(asr_server.manager.asr(b''))"
    ```
  - Output: `{'message': 'health ok'}` followed by an empty transcript.
  - Final status: interface import and health check pass; model baseline score expected to be poor because it always returns `""`.
- CV
  - Command:
    ```powershell
    $env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 --with fastapi==0.115.12 --with 'uvicorn[standard]==0.34.2' python -c "import sys; sys.path.insert(0, 'cv/src'); import cv_server; print(cv_server.health()); print(cv_server.manager.cv(b''))"
    ```
  - Output: `{'message': 'health ok'}` and `[]`.
  - Final status: interface import and health check pass; model baseline score expected to be `0.0` mAP because it returns no detections.
- Noise
  - Initial issue: `NoiseManager.noise()` attempted `Image.fromarray(img)` on a PIL image and only returned valid output through the exception fallback.
  - Fix: convert input with `.convert("RGB")` and save the PIL image directly.
  - Rerun command:
    ```powershell
    $env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 --with fastapi==0.115.12 --with 'uvicorn[standard]==0.34.2' --with pillow python -c "import sys, base64, io; from PIL import Image; sys.path.insert(0, 'noise/src'); import noise_server; buf=io.BytesIO(); Image.new('RGB',(2,2),(128,128,128)).save(buf, format='JPEG'); out=noise_server.manager.noise(buf.getvalue()); decoded=base64.b64decode(out); Image.open(io.BytesIO(decoded)).verify(); print('valid_jpeg', len(decoded))"
    ```
  - Output: `valid_jpeg 629`.
  - Final status: valid base64 JPEG output; no adversarial effect yet.
- NLP
  - Command:
    ```powershell
    $env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 --with fastapi==0.115.12 --with 'uvicorn[standard]==0.34.2' python -c "import sys; sys.path.insert(0, 'nlp/src'); import nlp_server; print(nlp_server.health()); nlp_server.manager.load_corpus([{'id':'DOC-1','document':'alpha'}]); print(nlp_server.manager.loaded); print(nlp_server.manager.qa('alpha?'))"
    ```
  - Output: `{'message': 'health ok'}`, `True`, and `{'documents': [], 'answer': ''}`.
  - Final status: interface import, health check, and load flag pass; QA baseline is empty.
- AE
  - Initial issue: `AEManager.ae()` always returned `0`, which can be illegal when `action_mask[0] == 0`.
  - Fix: choose first legal action from `(FORWARD, STAY, BACKWARD, LEFT, RIGHT, PLACE_BOMB)`.
  - Rerun command:
    ```powershell
    $env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 --with fastapi==0.115.12 --with 'uvicorn[standard]==0.34.2' python -c "import sys; sys.path.insert(0, 'ae/src'); import ae_server; print(ae_server.manager.ae({'action_mask':[0,0,0,0,1,0]})); print(ae_server.manager.ae({'action_mask':[0,0,0,1,0,0]})); print(ae_server.manager.ae({'action_mask':[1,1,1,1,1,0]}))"
    ```
  - Output: `4`, `3`, `0`.
  - Final status: returns legal actions for checked masks; policy remains a simple baseline.
