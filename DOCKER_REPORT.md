# Docker Report

Updated: 2026-05-14

## Environment

- Docker CLI command exists: `docker --version`
- Detected version: Docker `29.4.2`
- Docker daemon status: blocked locally.

Command attempted:

```powershell
docker ps
```

Result:

```text
WARNING: Error loading config file: open C:\Users\Harish kumar\.docker\config.json: Access is denied.
permission denied while trying to connect to the docker API at npipe:////./pipe/docker_engine
```

Action required:

Open Docker Desktop and wait until Docker is running, then rerun Docker validation.

## Image Names

- ASR: `brainhacknnn-asr`
- CV: `brainhacknnn-cv`
- Noise: `brainhacknnn-noise`
- NLP: `brainhacknnn-nlp`
- AE: `brainhacknnn-ae`

## Build Commands

```powershell
cd asr; docker build -t brainhacknnn-asr .
cd cv; docker build -t brainhacknnn-cv .
cd noise; docker build -t brainhacknnn-noise .
cd nlp; docker build -t brainhacknnn-nlp .
cd ae; docker build -t brainhacknnn-ae .
```

## Current Task Docker Status

| Task | Dockerfile | Entrypoint | Build Status | Smoke Status | Blocker |
| --- | --- | --- | --- | --- | --- |
| ASR | `asr/Dockerfile` | `uvicorn asr_server:app --port 5001 --host 0.0.0.0` | Not run | Not run | Docker daemon inaccessible |
| CV | `cv/Dockerfile` | `uvicorn cv_server:app --port 5002 --host 0.0.0.0` | Not run | Not run | Docker daemon inaccessible |
| Noise | `noise/Dockerfile` | `uvicorn noise_server:app --port 5003 --host 0.0.0.0` | Not run | Not run | Docker daemon inaccessible |
| NLP | `nlp/Dockerfile` | `uvicorn nlp_server:app --port 5004 --host 0.0.0.0` | Not run | Not run | Docker daemon inaccessible |
| AE | `ae/Dockerfile` | `uvicorn ae_server:app --port 5005 --host 0.0.0.0` | Not run | Not run | Docker daemon inaccessible |

## Smoke Test Commands After Docker Starts

```powershell
docker run --rm -p 5001:5001 brainhacknnn-asr
docker run --rm -p 5002:5002 brainhacknnn-cv
docker run --rm -p 5003:5003 brainhacknnn-noise
docker run --rm -p 5004:5004 brainhacknnn-nlp
docker run --rm -p 5005:5005 brainhacknnn-ae
```

Then query `/health` on the corresponding port.

## Official Build Commands

On GCP Workbench with the `til` CLI:

```bash
til build asr
til build cv
til build noise
til build nlp
til build ae
```
