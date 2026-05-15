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
| AE | `ae/Dockerfile` | `uvicorn ae_server:app --port 5005 --host 0.0.0.0` | Passed after latest AE policy change: `docker build -t brainhacknnn-ae .` | Passed after latest AE policy change: `/health` and `POST /ae` | None |
| NLP | `nlp/Dockerfile` | `uvicorn nlp_server:app --port 5004 --host 0.0.0.0` | Passed: `docker build -t brainhacknnn-nlp .` | Passed: `/health`, corpus load/poll, and QA | None |
| Noise | `noise/Dockerfile` | `uvicorn noise_server:app --port 5003 --host 0.0.0.0` | Passed: `docker build -t brainhacknnn-noise .` | Passed: `/health` and `POST /noise` | None |
| CV | `cv/Dockerfile` | `uvicorn cv_server:app --port 5002 --host 0.0.0.0` | Passed: `docker build -t brainhacknnn-cv .` | Passed: `/health` and `POST /cv` | None |
| ASR | `asr/Dockerfile` | `uvicorn asr_server:app --port 5001 --host 0.0.0.0` | Passed: `docker build -t brainhacknnn-asr .` | Passed: `/health` and `POST /asr` | None |

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
- Rebuilt successfully after the latest AE policy improvement.

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
- Re-smoke-tested successfully after the latest AE policy improvement.

## NLP Validation

Build command:

```powershell
docker build -t brainhacknnn-nlp .
```

Working directory:

```text
nlp/
```

Build result:

- Passed.
- Image: `brainhacknnn-nlp:latest`
- Docker warning only: JSON-form CMD recommended for signal handling.

Smoke commands:

```powershell
docker run -d --rm -p 5004:5004 --name brainhacknnn-nlp-smoke brainhacknnn-nlp
Invoke-RestMethod -Uri http://localhost:5004/health
Invoke-RestMethod -Method Post -Uri http://localhost:5004/nlp -ContentType 'application/json' -Body <tiny corpus JSON>
Invoke-RestMethod -Method Post -Uri http://localhost:5004/nlp -ContentType 'application/json' -Body <poll JSON>
Invoke-RestMethod -Method Post -Uri http://localhost:5004/nlp -ContentType 'application/json' -Body <question JSON>
docker stop brainhacknnn-nlp-smoke
```

Smoke result:

- `/health`: `{"message": "health ok"}`
- corpus load: `{"predictions": [{"status": "loading"}]}` followed by poll `loaded`
- QA: `{"predictions": [{"documents": ["DOC-1"], "answer": "Mars is red."}]}`
- Container stopped and removed.

## Noise Validation

Build command:

```powershell
docker build -t brainhacknnn-noise .
```

Working directory:

```text
noise/
```

Build result:

- Passed.
- Image: `brainhacknnn-noise:latest`
- Docker warning only: JSON-form CMD recommended for signal handling.

Smoke commands:

```powershell
docker run -d --rm -p 5003:5003 --name brainhacknnn-noise-smoke brainhacknnn-noise
Invoke-RestMethod -Uri http://localhost:5003/health
Invoke-RestMethod -Method Post -Uri http://localhost:5003/noise -ContentType 'application/json' -Body <tiny JPEG JSON>
docker logs brainhacknnn-noise-smoke --tail 80
docker stop brainhacknnn-noise-smoke
```

Smoke result:

- `/health`: `{"message": "health ok"}`
- `/noise`: returned one base64-encoded JPEG prediction for the tiny input image.
- Logs showed HTTP 200 for both smoke requests.
- Container stopped and removed.

## CV Validation

Build command:

```powershell
docker build -t brainhacknnn-cv .
```

Working directory:

```text
cv/
```

Build result:

- Passed.
- Image: `brainhacknnn-cv:latest`
- Docker warning only: JSON-form CMD recommended for signal handling.

Smoke commands:

```powershell
docker run -d --rm -p 5002:5002 --name brainhacknnn-cv-smoke brainhacknnn-cv
Invoke-RestMethod -Uri http://localhost:5002/health
Invoke-RestMethod -Method Post -Uri http://localhost:5002/cv -ContentType 'application/json' -Body <tiny JPEG JSON>
docker logs brainhacknnn-cv-smoke --tail 80
docker stop brainhacknnn-cv-smoke
```

Smoke result:

- `/health`: `{"message": "health ok"}`
- `/cv`: `{"predictions": [[]]}` for one tiny image, matching the current empty-detector baseline.
- Logs showed HTTP 200 for both smoke requests.
- Container stopped and removed.

## ASR Validation

Build command:

```powershell
docker build -t brainhacknnn-asr .
```

Working directory:

```text
asr/
```

Build result:

- Passed.
- Image: `brainhacknnn-asr:latest`
- Docker warning only: JSON-form CMD recommended for signal handling.

Smoke commands:

```powershell
docker run -d --rm -p 5001:5001 --name brainhacknnn-asr-smoke brainhacknnn-asr
Invoke-RestMethod -Uri http://localhost:5001/health
Invoke-RestMethod -Method Post -Uri http://localhost:5001/asr -ContentType 'application/json' -Body <tiny WAV JSON>
docker logs brainhacknnn-asr-smoke --tail 80
docker stop brainhacknnn-asr-smoke
```

Smoke result:

- `/health`: `{"message": "health ok"}`
- `/asr`: `{"predictions": [""]}` for one short silent WAV, matching the current empty-transcript baseline.
- Logs showed HTTP 200 for both smoke requests.
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
