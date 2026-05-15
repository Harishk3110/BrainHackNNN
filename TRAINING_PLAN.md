# Training Plan

Updated: 2026-05-15

## Global Training Position

No repo-local ASR, CV, or NLP competition datasets were detected. Do not start real training for those tasks until the exact dataset paths are provided or mounted. AE does not require a static dataset and is currently the only scored task with local measurable simulation.

## ASR

- Training data exists: no.
- Current model type: stub baseline in `asr/src/asr_manager.py`.
- Current inference behavior: returns `""`.
- Training command: blocked until audio/transcripts exist.
- Evaluation command:
  ```bash
  til test asr
  ```
  or, with server running and data present:
  ```bash
  python test/test_asr.py
  ```
- Expected artifact path: not established. Recommended future path: `asr/models/`.
- Model save/load path: not implemented.
- Hyperparameters: not applicable until model/data are chosen.
- Compute requirements: depends on chosen ASR model; prefer lightweight/faster inference model first.
- Fallback baseline if training impossible: keep valid interface returning normalized empty string; report missing ASR data.

## CV

- Training data exists: no.
- Current model type: stub baseline in `cv/src/cv_manager.py`.
- Current inference behavior: returns `[]`.
- Training command: blocked until COCO annotations/images exist.
- Evaluation command:
  ```bash
  til test cv
  ```
  or, with server running and data present:
  ```bash
  python test/test_cv.py
  ```
- Expected artifact path: not established. Recommended future path: `cv/models/`.
- Model save/load path: not implemented.
- Hyperparameters: confidence threshold, IoU/NMS threshold, image size once detector exists.
- Compute requirements: detector training likely requires GPU; do not add heavy detector dependencies without data and a smoke run.
- Fallback baseline if training impossible: keep valid empty detection output; report missing CV data.

## NLP

- Training data exists: no repo-local official data.
- Current model type: dependency-light lexical RAG/extractive baseline.
- Current inference behavior:
  - loads corpus documents into token index.
  - returns top positively scored documents.
  - returns best matching sentence as grounded answer.
  - returns empty docs/answer when no lexical evidence exists.
- Training command: none; no learned model currently.
- Evaluation command:
  ```bash
  til test nlp
  ```
  or, with server running and data present:
  ```bash
  python test/test_nlp.py
  ```
- Expected artifact path: none for current baseline.
- Model save/load path: none for current baseline.
- Hyperparameters:
  - stopword set
  - TF-IDF-style scoring
  - max returned documents: 3
  - answer max length: 300 chars
- Compute requirements: CPU only.
- Fallback baseline if training impossible: current lexical RAG baseline.

## AE

- Training data exists: not required.
- Current model type: deterministic heuristic policy.
- Current policy:
  - reset recent-location memory when `step == 0`.
  - choose legal actions only.
  - target visible mission/resource/recon tiles.
  - use recent-location memory to reduce loops when no reward tile is visible.
- Training command: no RL training currently; heuristic iteration is preferred until a training loop shows measurable benefit.
- Evaluation command:
  ```bash
  til test ae
  ```
  or local simulation through:
  ```powershell
  $env:UV_CACHE_DIR='.uv-cache'; uv run --no-project --python 3.11 --with ./til-26-ae python -c "<seeded AE simulation harness>"
  ```
- Expected artifact path: none for heuristic policy.
- Model save/load path: none.
- Hyperparameters:
  - recent memory length: `12`
  - visible tile reward weights: mission `5`, resource `2`, recon `1`
  - target score: `reward * 10 - distance`
- Compute requirements: CPU only for heuristic simulation.
- Fallback baseline if training impossible: current heuristic policy.

## Adversarial Noising

- Training data exists: no CV images locally.
- Current model type: valid JPEG passthrough/re-encode baseline.
- Current inference behavior: decodes input image, converts to RGB, saves as JPEG, returns base64.
- Training command: none.
- Evaluation command:
  ```bash
  til test noise
  ```
  or, with server running and CV data present:
  ```bash
  python test/test_noise.py
  ```
- Expected artifact path: none.
- Model save/load path: none.
- Hyperparameters: JPEG settings and perturbation strategy if changed later.
- Compute requirements: CPU.
- Fallback baseline if no data: current valid output baseline.
