# Submission Checklist

Updated: 2026-05-15

## Git

- Branch: `main`
- Remote: `https://github.com/Harishk3110/BrainHackNNN.git`
- Latest pushed kept experiment: `2092c5d experiment(ae): turn when movement repeats`

## Docker Images

- `brainhacknnn-asr`
- `brainhacknnn-cv`
- `brainhacknnn-noise`
- `brainhacknnn-nlp`
- `brainhacknnn-ae`

Docker build validation passed locally for all five images when Docker commands were run with approved daemon access.

## Build Commands

Manual Docker:

```powershell
cd asr; docker build -t brainhacknnn-asr .
cd cv; docker build -t brainhacknnn-cv .
cd noise; docker build -t brainhacknnn-noise .
cd nlp; docker build -t brainhacknnn-nlp .
cd ae; docker build -t brainhacknnn-ae .
```

Official `til` CLI on GCP Workbench:

```bash
til build asr
til build cv
til build noise
til build nlp
til build ae
```

## Test Commands

```bash
til test asr
til test cv
til test noise
til test nlp
til test ae
```

Direct evaluator scripts with servers running and `/home/jupyter/{TEAM_TRACK}` data present:

```bash
python test/test_asr.py
python test/test_cv.py
python test/test_noise.py
python test/test_nlp.py
python test/test_ae.py
```

Local AE sanity:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python scripts\eval_ae_local.py --seeds 0 1 2 3 4
```

## Submit Commands

```bash
til submit asr
til submit cv
til submit noise
til submit nlp
til submit ae
```

## Latest Local Metrics

- AE local deterministic reward: average `149.000` over seeds `0..4`.
- AE invalid actions: `0.000`.
- AE repeated locations: `176.000`.
- NLP synthetic hit/miss checks pass.
- Noise synthetic valid-JPEG check passes.
- ASR official metric blocked by missing data.
- CV official metric blocked by missing data.

## Latest Training Artifacts

- ASR: none.
- CV: none.
- NLP: none; dependency-light lexical RAG code only.
- AE: code-only heuristic policy in `ae/src/ae_manager.py`.
- Noise: none.

## Known Limitations

- Missing local official datasets under `/home/jupyter/{TEAM_TRACK}`.
- `til` CLI is not available in this local Windows shell.
- Global `python` and `pip` are not on PATH; `uv` is used for local checks.
- Docker daemon access requires approved Docker commands from this environment.
- ASR and CV are still valid interface baselines but not accuracy models.
- NLP official score cannot be measured without NLP data/evaluator assets.

## Missing Data Warnings

Provide exact paths for:

- ASR audio/transcripts.
- CV COCO annotations and images.
- NLP questions/documents/evaluator model assets.

## Recommended Submit Order

1. AE: highest value and currently best locally measured improvement.
2. NLP: dependency-light improvement over empty baseline.
3. Noise: valid output baseline.
4. CV: valid but expected low score without detector/data.
5. ASR: valid but expected low score without ASR model/data.

## Final Readiness Criteria

- Git status clean.
- All commits pushed.
- Docker builds complete for all five images. Done.
- All five `/health` endpoints pass inside containers.
- Official `til test` run recorded for each task on GCP Workbench.
- Metrics copied into `METRICS_REPORT.md`.
- Known missing data warnings resolved or accepted.
