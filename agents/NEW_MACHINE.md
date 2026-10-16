# New machine checkout

Remote (public):

```text
https://github.com/brianpatrickreavey/oscal-processor.git
```

```bash
git clone https://github.com/brianpatrickreavey/oscal-processor.git
cd oscal-processor
```

## Toolchain

| Tool | Notes |
|---|---|
| Python 3.13 (pyenv `3.13.0` is what README used) | FastAPI app |
| pip | `requirements.txt` |
| Docker | optional; `./start.sh` / `./stop.sh` |
| pytest | `tests/` |

```bash
pyenv shell 3.13.0   # if you use pyenv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Local FastAPI (current development path):

```bash
uvicorn src.api.main:app --reload
```

UI: http://localhost:8000 — served from `static/index_claude.html`.

Docker (`./start.sh`) builds `Dockerfile`, which still starts Python `http.server` against `src/webserver/` (empty). Prefer uvicorn until that image is updated.

## Tests

```bash
pytest tests/
```

Manual API scripts live in `scripts/` and `tests/manual/`.

## What is in git vs local

**In git:** source (`src/`), UI (`static/`), NIST catalog YAML, example SSPs, PRD, tests, agent briefing.

**Not in git:** `.venv/`, `temp/` (including `rendered.yaml` and webserver logs), `__pycache__`, `.pytest_cache`.
