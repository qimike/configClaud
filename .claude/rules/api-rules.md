---
paths:
  - "src/api/**/*"
---

# API Rules

These rules apply automatically whenever a file under `src/api/` is in Claude
Code's context (for example `src/api/sample_api.py`). They refine — but do not
replace — the baseline standards in the project-level `CLAUDE.md`.

## Rules

- **FastAPI preferred** — use FastAPI for HTTP endpoints.
- **Input validation required** — validate every request body/query/path
  parameter with Pydantic models; never trust raw input.
- **Return typed response models** — every endpoint declares a
  `response_model` and returns that type.
- **No business logic in controllers** — controllers only wire requests to a
  service layer and translate errors into HTTP responses. Business rules live in
  a service/domain layer.

## Which files load this rule

| File | Loads this rule? | Why |
| --- | --- | --- |
| `src/api/sample_api.py` | ✅ Yes | Matches `src/api/**/*` |
| `src/frontend/sample_ui.ts` | ❌ No | Outside `src/api/` |
| `src/tests/sample_api.test.py` | ❌ No | Outside `src/api/` (loads testing rules instead) |
