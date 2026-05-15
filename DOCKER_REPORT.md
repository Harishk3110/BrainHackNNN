# Docker Report

Updated: 2026-05-15

## Environment

- Docker CLI command exists: `docker --version`
- Detected version: Docker `29.4.2`
- Docker daemon status: available when Docker commands are run with approved daemon access from this environment.

Command attempted:

```powershell
docker ps
```

Previous result:

```text
WARNING: Error loading config file: open C:\Users\Harish kumar\.docker\config.json: Access is denied.
permission denied while trying to connect to the docker API at npipe:////./pipe/docker_engine
```

Current result with approved Docker daemon access:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## Image Names

- ASR: `brainhacknnn-asr`
- CV: `brainhacknnn-cv`
- Noise: `brainhacknnn-noise`
- NLP: `brainhacknnn-nlp`
- AE: `brainhacknnn-ae`

## Build Commands

```powershell
cd ae; docker build -t brainhacknnn-ae .
cd nlp; docker build -t brainhacknnn-nlp .
cd noise; docker build -t brainhacknnn-noise .
cd cv; docker build -t brainhacknnn-cv .
cd asr; docker build -t brainhacknnn-asr .
```

## Current Task Docker Status

| Task | Dockerfile | Entrypoint | Build Status | Smoke Status | Blocker |
| --- | --- | --- | --- | --- | --- |
| AE | `ae/Dockerfile` | `uvicorn ae_server:app --port 5005 --host 0.0.0.0` | Passed: `docker build -t brainhacknnn-ae .` | Passed: `/health` and `POST /ae` | None |
| NLP | `nlp/Dockerfile` | `uvicorn nlp_server:app --port 5004 --host 0.0.0.0` | Not run | Not run | Await AE result |
| Noise | `noise/Dockerfile` | `uvicorn noise_server:app --port 5003 --host 0.0.0.0` | Not run | Not run | Await NLP result |
| CV | `cv/Dockerfile` | `uvicorn cv_server:app --port 5002 --host 0.0.0.0` | Not run | Not run | Await Noise result |
| ASR | `asr/Dockerfile` | `uvicorn asr_server:app --port 5001 --host 0.0.0.0` | Not run | Not run | Await CV result |

## Smoke Test Commands

```powershell
docker run --rm -p 5005:5005 brainhacknnn-ae
docker run --rm -p 5004:5004 brainhacknnn-nlp
docker run --rm -p 5003:5003 brainhacknnn-noise
docker run --rm -p 5002:5002 brainhacknnn-cv
docker run --rm -p 5001:5001 brainhacknnn-asr
```

Then query `/health` on the corresponding port.

## AE Validation

Build command:

```powershell
docker build -t brainhacknnn-ae .
```

Working directory:

```text
ae/
```

Build result:

- Passed.
- Image: `brainhacknnn-ae:latest`
- Docker warning only: JSON-form CMD recommended for signal handling.

Smoke commands:

```powershell
docker run -d --rm -p 5005:5005 --name brainhacknnn-ae-smoke brainhacknnn-ae
Invoke-RestMethod -Uri http://localhost:5005/health
$body = @{ instances = @(@{ observation = @{ step = 0; location = @(0,0); direction = 0; action_mask = @(0,0,0,0,1,0) } }) } | ConvertTo-Json -Depth 8
Invoke-RestMethod -Method Post -Uri http://localhost:5005/ae -ContentType 'application/json' -Body $body
docker stop brainhacknnn-ae-smoke
```

Smoke result:

- `/health`: `{"message": "health ok"}`
- `/ae`: `{"predictions": [{"action": 4}]}`
- Container stopped and removed.

## Official Build Commands

On GCP Workbench with the `til` CLI:

```bash
til build asr
til build cv
til build noise
til build nlp
til build ae
```
