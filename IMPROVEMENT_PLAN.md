# Improvement Plan

Created: 2026-05-14

## Ranked Priorities

1. AE: highest value because it is 40% of total score. First goal is a valid, deterministic, map-aware heuristic that improves reward without adding dependencies.
2. NLP: high quick-win potential with lightweight lexical retrieval and extractive answer snippets. Avoid heavy LLM dependencies until local data/metrics justify them.
3. CV: current baseline returns no detections. Meaningful gains likely require either training data priors, a small detector, or leveraging allowed pretrained assets if available in the competition environment.
4. ASR: current baseline returns empty strings. Real gains likely require a speech model or track-specific assets; dependency/runtime cost must be measured.
5. Noise: keep outputs valid and within fairness thresholds. It is not directly scored in qualifiers, so avoid risky perturbations until scored tasks improve.

## Quick Wins

- AE
  - Improve action validity and survival behavior with `action_mask`, health, frozen state, and local tile observations.
  - Add small deterministic exploration memory reset on `step == 0`.
  - Prefer resource/challenge tiles visible in `agent_viewcone`; otherwise avoid repeated backtracking.
  - Files likely to change: `ae/src/ae_manager.py`.
  - Metric: average reward / score from `test/test_ae.py`.
  - Validation: `til test ae` or `python test/test_ae.py` with `til_environment` installed.
  - Rollback: revert `ae/src/ae_manager.py`.
- NLP
  - Store corpus documents and return top document IDs by token overlap / BM25-style scoring.
  - Generate short extractive answers from best matching sentence rather than always empty.
  - Files likely to change: `nlp/src/nlp_manager.py`.
  - Metric: NLP RAG QA Accuracy and runtime.
  - Validation: `til test nlp` or `python test/test_nlp.py`.
  - Rollback: revert `nlp/src/nlp_manager.py`.
- Noise
  - Preserve valid JPEG output and avoid exception fallback.
  - Files likely to change: `noise/src/noise_manager.py`.
  - Metric: Noise pass rate.
  - Validation: `til test noise` or `python test/test_noise.py`.
  - Rollback: revert `noise/src/noise_manager.py`.

## Medium-Effort Improvements

- AE
  - Build a local coordinate memory from observed viewcone and base viewcone.
  - Add goal selection: resource collection, challenge interaction, base defense, and bomb placement only when legal and useful.
  - Add anti-loop behavior from recent locations/actions.
- NLP
  - Add chunking with sentence windows and compact TF-IDF scoring implemented with the standard library.
  - Tune number of returned documents and answer length against evaluator behavior.
- CV
  - Inspect training annotations when available and implement a data-prior baseline if object positions/classes are structured.
  - If allowed assets exist locally, wire a lightweight pretrained detector with thresholds tuned for mAP.
- ASR
  - Inspect available audio/transcript training data when present.
  - If a speech model is available in the environment, add batched inference and transcript normalization.

## Risky / High-Reward Ideas

- AE: train or load a policy using `til_environment`; risk is time, dependency setup, and overfitting without stable evaluation.
- NLP: use a transformer QA/retrieval model; risk is container size and inference latency.
- CV: add YOLO/RT-DETR or similar detector; risk is heavy dependencies, model weight availability, and Docker build time.
- ASR: add Whisper/faster-whisper; risk is model download/weights, GPU availability, memory, and speed.
- Noise: adversarial perturbation against a surrogate detector; risk is failing fairness thresholds and not helping qualifier score.

## Metrics To Track

- AE: total rewards, normalized score, average runtime per round.
- NLP: RAG QA Accuracy, corpus load time, QA latency.
- CV: mAP@.5:.05:.95, average images/sec.
- ASR: 1 - MER, per-language WER/CER, audio/sec.
- Noise: pass rate, L2 RMSE, L2 inside, SSIM inside.

## Validation Commands

Official preferred commands:

```bash
til test ae
til test nlp
til test cv
til test asr
til test noise
```

Direct commands when service containers are already running:

```bash
python test/test_ae.py
python test/test_nlp.py
python test/test_cv.py
python test/test_asr.py
python test/test_noise.py
```

Local lightweight syntax/interface check:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.14 python -m py_compile asr\src\asr_manager.py asr\src\asr_server.py cv\src\cv_manager.py cv\src\cv_server.py noise\src\noise_manager.py noise\src\noise_server.py nlp\src\nlp_manager.py nlp\src\nlp_server.py ae\src\ae_manager.py ae\src\ae_server.py
```

## Rollback Plan

- Keep each experiment to one task and the fewest files possible.
- Before each experiment, check `git status` and the experiment log.
- If validation is worse or broken, revert only the files touched by that experiment.
- Commit only kept changes with the required format: `experiment(<task>): short description`.
- Do not change Docker entrypoints unless an entrypoint-specific failure is proven.
