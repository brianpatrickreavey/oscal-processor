# oscal-processor — project context

Render and edit OSCAL catalogs and System Security Plans (SSPs) in a local web UI, then publish (GitHub Pages / Confluence planned, not built).

## Stack

- Python FastAPI (`src/api/main.py`), Pydantic, PyYAML
- Static UI in `static/` (`index_claude.html` is what `/` currently serves)
- NIST SP-800-53 rev5 catalog: `src/data/NIST_SP-800-53_rev5_catalog.yaml` (~7MB)
- Example SSP YAML: `src/data/ssp-example.yaml`
- Runtime/editor SSP JSON written under `data/`
- Tests: `tests/test_api.py` plus manual scripts

## Layout

```text
src/api/          FastAPI routers (system characteristics, inventory, controls, …)
src/utils/        data_store, json_io, processor
src/data/         catalog + example SSP
static/           web UI (index.html, index_claude.html, new_index.html)
data/             SSP JSON produced by the editor
docs/             wireframe.png / .svg
PRD.md            product requirements
NOTES.md          open UI questions (tabs, system implementation nesting)
```

## Current state

- FastAPI + Claude-era HTML UI exist; publisher plugins do not.
- `Dockerfile` / `start.sh` still assume a static `http.server` in `src/webserver/` (empty). Dev run is uvicorn.
- Open notes in `NOTES.md`: component list UX, whether system implementation children nest under that section, control implementations will be the bulk of the UI.

## Commands

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
pytest tests/
./start.sh    # docker, outdated vs FastAPI
./stop.sh
```
