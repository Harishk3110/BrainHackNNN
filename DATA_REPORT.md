# Data Report

Updated: 2026-05-15

## Environment Summary

- Repository root: `C:\Users\Harish kumar\Desktop\DSTA\til-26`
- Git remote `origin`: `https://github.com/Harishk3110/BrainHackNNN.git`
- Global `python` / `pip`: not available on PATH.
- `uv`: available (`uv 0.11.7`), usable with repo-local cache via `$env:UV_CACHE_DIR='.uv-cache'`.
- Docker CLI: installed.
- Docker daemon: available when Docker commands are run with approved daemon access from this environment.

## Detected Repo Data / Assets

Detected by searching for `data`, `datasets`, `sample`, `samples`, `train`, `val`, `validation`, `test`, `assets`, `annotations`, `labels`, `.csv`, `.json`, `.jsonl`, `.wav`, `.mp3`, `.flac`, `.jpg`, `.jpeg`, `.png`.

Latest targeted scan on 2026-05-15 excluded `.uv-cache` and `__pycache__` so dependency-cache examples are not counted as competition data.

- `test/test_asr.py`: official ASR local evaluator script.
- `test/test_cv.py`: official CV local evaluator script.
- `test/test_noise.py`: official noising local evaluator script.
- `test/test_nlp.py`: official NLP local evaluator script.
- `test/test_ae.py`: official AE local evaluator script.
- `test/test_utils.py`: shared evaluator batching helper.
- `test/noise_eval/eval_thresholds_v2.yaml`: noising fairness thresholds.

No repo-local ASR audio/transcript files, CV images/annotations, or NLP question/document datasets were found in the current targeted recheck.

Targeted scan results:

- ASR audio/transcripts: none found. Matches were source/evaluator files only: `asr/src/asr_server.py`, `asr/src/asr_manager.py`, `test/test_asr.py`.
- CV images/annotations: none found.
- NLP docs/questions: none found. Matches were source/evaluator/requirements files only, not datasets.
- Dataset-like directories: none found outside dependency caches.

## Expected Data Formats

### ASR

Expected official path:

- `/home/jupyter/{TEAM_TRACK}/asr/asr.jsonl`
- Audio files referenced by each JSONL row under `/home/jupyter/{TEAM_TRACK}/asr`

Expected fields from `test/test_asr.py`:

- `key`
- `audio`
- `transcript`
- `language`

Local train/val/test status: missing.

Can train locally now: no.

### CV

Expected official path:

- `/home/jupyter/{TEAM_TRACK}/cv/annotations.json`
- `/home/jupyter/{TEAM_TRACK}/cv/images`

Expected format: COCO-style annotations with `images` and `annotations`.

Local train/val/test status: missing.

Can train locally now: no.

### Adversarial Noising

Expected official path:

- Uses CV data from `/home/jupyter/{TEAM_TRACK}/cv`.
- Threshold config exists locally at `test/noise_eval/eval_thresholds_v2.yaml`.

Local train/val/test status: image data missing; threshold script/config present.

Can train locally now: no training needed; full validation blocked by missing CV images.

### NLP

Expected official path:

- `/home/jupyter/{TEAM_TRACK}/nlp/nlp.jsonl`
- `/home/jupyter/{TEAM_TRACK}/nlp/documents/*.txt`
- Optional evaluator model copied from `/home/jupyter/{TEAM_TRACK}/nlp/models/nlp_eval_512.zip` if local `test/models/nlp_eval_512` is absent.

Expected fields from `test/test_nlp.py`:

- Question rows: `question`, `answer`, `source_docs`
- Documents: text files whose stem is the document ID.

Local train/val/test status: missing.

Can train locally now: no. Lightweight synthetic sanity checks are possible.

### AE

Expected data:

- No static dataset required for policy simulation.
- Uses `til-26-ae` submodule package `til_environment`.

Detected path:

- `til-26-ae/til_environment`

Local train/val/test status: simulation environment available through `uv --with ./til-26-ae`.

Can train locally now: limited policy evaluation is possible. Full RL training is possible only if we choose to implement it, but current priority is deterministic heuristic policy because it is fast and measurable.

## Missing Paths

These are required for full official local evaluation:

- `/home/jupyter/{TEAM_TRACK}/asr/asr.jsonl`
- `/home/jupyter/{TEAM_TRACK}/asr/<audio files>`
- `/home/jupyter/{TEAM_TRACK}/cv/annotations.json`
- `/home/jupyter/{TEAM_TRACK}/cv/images`
- `/home/jupyter/{TEAM_TRACK}/nlp/nlp.jsonl`
- `/home/jupyter/{TEAM_TRACK}/nlp/documents`
- `/home/jupyter/{TEAM_TRACK}/nlp/models/nlp_eval_512.zip` or local `test/models/nlp_eval_512`

Needed from user if outside repo:

- Exact local path to ASR data.
- Exact local path to CV image/annotation data.
- Exact local path to NLP question/document data.

Exact expected local layouts if data is provided:

- ASR: directory containing `asr.jsonl` plus the referenced audio files.
- CV: directory containing `annotations.json` and an `images/` subdirectory.
- NLP: directory containing `nlp.jsonl`, `documents/`, and optionally `models/nlp_eval_512.zip`.

## Task Trainability Now

- ASR: cannot train locally; missing audio/transcripts.
- CV: cannot train locally; missing labeled images.
- Noise: can validate image-format behavior with synthetic images; full threshold validation requires CV images/annotations.
- NLP: can improve dependency-light RAG logic with synthetic checks; cannot evaluate official score without NLP data/evaluator model.
- AE: can evaluate seeded simulations locally with `til_environment`; this is the only currently measurable scored task.
