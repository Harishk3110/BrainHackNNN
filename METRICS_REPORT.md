# Metrics Report

Updated: 2026-05-14

## Current Metric Availability

- Full official metrics for ASR, CV, NLP, and Noise require `/home/jupyter/{TEAM_TRACK}` datasets and running task servers.
- AE simulation is locally available through `uv --with ./til-26-ae`.
- Synthetic sanity metrics are available for NLP and Noise.
- Docker-based smoke/runtime metrics are blocked until Docker Desktop is running.

## ASR Metrics

Official evaluator: `test/test_asr.py`

Implemented/verified metrics:

- Word Error Rate through `jiwer.wer` for English, Malay, Tamil.
- Character Error Rate through `jiwer.cer` for Chinese.
- Transcript normalization:
  - lowercase
  - dash substitution
  - punctuation removal
  - whitespace stripping/reduction
- Overall score: `1 - mean_error_rate` across English, Chinese, Malay, Tamil.

Runtime metrics:

- Not currently measured by official script beyond total script runtime.
- To measure latency per file, wrap requests inside `test/test_asr.py` or a local sanity script once data/server exists.

Current local result:

- Official metric blocked: missing ASR data and no running ASR server.
- Baseline manager returns `""` for every file.

## CV Metrics

Official evaluator: `test/test_cv.py`

Implemented/verified metrics:

- COCO mAP via `pycocotools.COCOeval`.
- Empty predictions return `0.0` mAP.

Runtime metrics:

- Not currently measured by official script beyond total script runtime.
- Latency per image can be measured around request batches once data/server exists.

Current local result:

- Official metric blocked: missing CV annotations/images and no running CV server.
- Baseline manager returns `[]` for every image.

## NLP Metrics

Official evaluator: `test/test_nlp.py`

Implemented/verified metrics:

- Retrieval overlap: at least one overlap between ground-truth `source_docs` and predicted top-3 docs.
- Answer-equivalence model score where retrieval overlaps.
- Special no-answer/false-premise handling:
  - both docs and answers empty can score as correct.
  - empty answer with document overlap can receive retrieval-only score depending on ground truth.

Local sanity checks run:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile nlp\src\nlp_manager.py
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -c "<synthetic hit/miss/stopword-only QA checks>"
```

Current local synthetic result:

- Positive query: `{'documents': ['DOC-1'], 'answer': 'The red key is under the garden bench.'}`
- No-match query: `{'documents': [], 'answer': ''}`
- Stopword-only query: `{'documents': [], 'answer': ''}`

Official score:

- Blocked: missing `/home/jupyter/{TEAM_TRACK}/nlp` data and evaluator model path.

## AE Metrics

Official evaluator: `test/test_ae.py`

Official metric:

- `score = total_rewards / NUM_ROUNDS / MAX_SCORE`
- `NUM_ROUNDS = 6`
- `MAX_SCORE = 1000`

Local deterministic simulation metric:

- Score per seed using `til_environment`.
- Average reward over fixed seeds.
- Runtime of simulation comparison.
- Invalid actions: action mask is checked by policy; targeted synthetic checks verify legal fallback. A dedicated counter is not yet wired into the local comparison harness.
- Repeated-location count: policy tracks recent locations internally; a dedicated external metric is not yet wired into the local comparison harness.

Current best local AE result:

- Previous legal-forward baseline: `0.0` reward on seeds `0..2` with stationary other agents.
- Visible reward targeting: `55.0` reward on seeds `0..2`.
- Recent-location exploration: `84.0` reward on seeds `0..4`.
- Reverted experiments:
  - opportunistic bomb placement: neutral at `84.0` vs `84.0`.
  - target weighting multiplier change: neutral at `84.0` vs `84.0`.

Current best policy:

- `ae/src/ae_manager.py`
- Chooses legal actions.
- Steers toward visible mission/resource/recon tiles.
- Uses recent-location memory to reduce loops when no reward tile is visible.

## Noising Metrics

Official evaluator: `test/test_noise.py`

Implemented/verified metrics:

- Valid base64 image output.
- Valid JPEG decode.
- Threshold/fairness script exists:
  - `L2 (RMSE) <= 67`
  - `L2 inside <= 50`
  - `SSIM inside >= 0.3`
- Full pipeline computes:
  - global RMSE
  - inside-box RMSE
  - inside-box SSIM
  - image-level fairness pass rate

Local sanity result:

- Synthetic 2x2 RGB JPEG round trip produced valid JPEG output.

Official score:

- Blocked: missing CV images/annotations and no running Noise server.

## Current Best Metrics Summary

- AE: best measured local deterministic reward `84.0` on seeds `0..4` with stationary other agents.
- NLP: synthetic retrieval/answer checks pass; official score unavailable.
- Noise: synthetic valid-JPEG check passes; official pass rate unavailable.
- ASR: official score unavailable; baseline expected poor due to empty transcript output.
- CV: official score unavailable; baseline expected `0.0` mAP due to empty detections.
