# Agent Instructions

Read [`agents/README.md`](agents/README.md) first. On a new machine, follow [`agents/NEW_MACHINE.md`](agents/NEW_MACHINE.md). Project context: [`agents/PROJECT.md`](agents/PROJECT.md).

Treat questions as read-only. Do not edit, commit, or push unless the user uses explicit action language.

## Build & Test

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
pytest tests/
```

UI: http://localhost:8000 (`static/index_claude.html`).

## Architecture

FastAPI backend + static HTML UI for OSCAL catalog/SSP editing. See `PRD.md` and `agents/PROJECT.md`.
