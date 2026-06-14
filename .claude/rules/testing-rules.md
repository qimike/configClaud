---
paths:
  - "**/*.test.*"
---

# Testing Rules

These rules apply automatically whenever a test file matching `**/*.test.*` is in
Claude Code's context (for example `src/tests/sample_api.test.py`). They refine —
but do not replace — the baseline Testing Standards in the project-level
`CLAUDE.md`.

## Rules

- **AAA pattern** — structure each test as Arrange / Act / Assert, with the
  sections visually separated.
- **Test names must describe behaviour** — e.g.
  `test_create_user_rejects_duplicate_email`, not `test_create_user_2`.
- **Mock external dependencies** — databases, network calls, and other services
  must be mocked so tests are deterministic and isolated.

## Which files load this rule

| File | Loads this rule? | Why |
| --- | --- | --- |
| `src/tests/sample_api.test.py` | ✅ Yes | Matches `**/*.test.*` |
| `src/frontend/sample_ui.ts` | ❌ No | Not a `*.test.*` file |
| `src/api/sample_api.py` | ❌ No | Not a `*.test.*` file (loads API rules instead) |
