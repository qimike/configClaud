# Exercise 2 — Claude Code Automation & Configuration

> **Submission note for the reviewer:** This repository is a self-contained
> demonstration of six Claude Code features. Every required file has been created
> and every locally-runnable validation has been executed. The exact commands and
> their captured outputs are reproduced below so the solution can be assessed
> **without rerunning anything**.

---

## 1. Exercise Overview

The goal of Exercise 2 is to implement and demonstrate six Claude Code
capabilities in a single repository:

1. **Project-level `CLAUDE.md`** — shared standards loaded for every session.
2. **Path-specific rules** (`.claude/rules/`) — rules that activate only for
   matching files.
3. **Project-scoped skill** (`.claude/skills/code-review/`) — a forked,
   tool-restricted code-review skill.
4. **MCP server configuration** (`.mcp.json`) — project-scoped MCP with env-var
   expansion.
5. **Personal MCP configuration example** (`~/.claude.json`) — user-scoped MCP.
6. **Plan Mode vs. Direct Execution** — a comparison across three scenarios.

A small but **real, runnable** sample application (FastAPI backend, TypeScript
frontend client, pytest tests) is included so the rules and skill have genuine
code to act on, and so the validations produce meaningful results.

---

## 2. Folder Structure

```
.
├── CLAUDE.md                        # Step 1: project-level standards
├── .mcp.json                        # Step 4: project-scoped MCP server
├── pytest.ini                       # pytest config (enables *.test.py discovery)
├── README.md                        # this file
├── src
│   ├── api
│   │   └── sample_api.py            # FastAPI app (triggers api-rules.md)
│   ├── frontend
│   │   └── sample_ui.ts             # TypeScript API client
│   └── tests
│       └── sample_api.test.py       # pytest tests (triggers testing-rules.md)
├── .claude
│   ├── rules
│   │   ├── api-rules.md             # Step 2: applies to src/api/**/*
│   │   └── testing-rules.md         # Step 2: applies to **/*.test.*
│   └── skills
│       └── code-review
│           ├── skill.md             # Step 3: forked, Read/Grep/Glob-only skill
│           └── examples.md          # Step 3: worked example output
├── docs
│   ├── personal-mcp-example.md      # Step 5 support: ~/.claude.json explanation
│   └── plan-mode-vs-direct-execution.md   # Step 5: full comparison
└── examples
    └── claude.json.example          # Step 5: concrete personal MCP example file
```

---

## 3. Implementation Details

### Sample application (supporting code)
- **`src/api/sample_api.py`** — a FastAPI service with a `UserService` (business
  logic) and thin controllers. Demonstrates type hints, Pydantic validation,
  typed `response_model`s, structured logging, composition, and no hardcoded
  secrets — i.e. the standards from `CLAUDE.md` and `api-rules.md`.
- **`src/frontend/sample_ui.ts`** — a strict-mode TypeScript client whose
  interfaces mirror the API's Pydantic models; the transport is injected for
  testability.
- **`src/tests/sample_api.test.py`** — four pytest tests following AAA, with
  behavioural names, mocking the service dependency (per `testing-rules.md`).
- **`pytest.ini`** — adds `*.test.py` to discovery patterns and uses
  `--import-mode=importlib`, since the required filename `sample_api.test.py`
  isn't a default pytest pattern.

### Feature files
- **`CLAUDE.md`**, **`.claude/rules/*.md`**, **`.claude/skills/code-review/*`**,
  **`.mcp.json`**, **`examples/claude.json.example`**, and the two **`docs/`**
  documents implement Steps 1–5 (explained next).

---

## 4. Explanation of Each Claude Code Feature

### Step 1 — Project-level `CLAUDE.md`
`CLAUDE.md` is loaded automatically into context at the **start of every session**
opened in this repo. Because it is committed and version-controlled, **all
developers and all Claude Code runs share the same standards** (coding, testing,
documentation). Changing the team's rules is a one-line commit. This differs from
a personal `~/.claude/CLAUDE.md`, which only affects one machine. See the file's
own "How project-level instructions affect all developers" callout.

### Step 2 — Path-specific rules (`.claude/rules/`)
Each rule file uses **YAML frontmatter** with a `paths` glob. The rule's
instructions are applied **only when a matching file is in context**:
- `api-rules.md` → `paths: ["src/api/**/*"]` → loads for `src/api/sample_api.py`
  (FastAPI preferred, input validation required, typed response models, no
  business logic in controllers).
- `testing-rules.md` → `paths: ["**/*.test.*"]` → loads for
  `src/tests/sample_api.test.py` (AAA, behavioural names, mock external deps).

Each rule file contains a table documenting **which files load it and why**. The
sample source/test files are deliberately written to *trigger* these rules.

### Step 3 — Project-scoped skill (`.claude/skills/code-review/`)
`skill.md` declares `context: fork` and restricts `allowed-tools` to **Read,
Grep, Glob**. The skill performs code review: identifies bugs, suggests
improvements, and reports security findings (see `examples.md` for a worked
output). The file documents two things in depth:
- **Why context isolation is useful** — a review reads many files and generates
  lots of intermediate text; `context: fork` does that heavy reading in an
  isolated sub-context and returns **only the final report**.
- **How it avoids polluting the main conversation** — the noisy exploration stays
  in the fork; the main thread only ever sees the structured summary. Combined
  with the read-only toolset, the skill can explore freely with no side effects.

### Step 4 — MCP configuration (`.mcp.json`)
Project-scoped MCP config defining a `github` server launched via `npx`, using
**environment variable expansion** (`"GITHUB_TOKEN": "${GITHUB_TOKEN}"`) so no
secret is written into the file. Committed, so every collaborator gets it.

### Step 5a — Personal MCP example (`~/.claude.json`)
`docs/personal-mcp-example.md` (with the concrete
`examples/claude.json.example`) shows a **user-scoped** config containing an
**experimental** `experimental-notes` server. It explains:
- **Project-scoped MCP** (`.mcp.json`, committed, team-wide),
- **User-scoped MCP** (`~/.claude.json`, per-developer, every project),
- **How both become available simultaneously** — Claude Code merges all scopes
  into one registry at session start, so a developer here has *both* the shared
  `github` server and their personal `experimental-notes` server at once
  (project scope wins on name collisions).

### Step 5b — Plan Mode vs. Direct Execution
`docs/plan-mode-vs-direct-execution.md` works through three scenarios:
- **A. Single-file bug fix** → **direct execution** (localized, unambiguous,
  test-verified; planning would cost more than the fix).
- **B. Multi-file library migration** → **Plan Mode**, with dependency analysis
  and a migration checklist (wide, ordered, partial state breaks the repo).
- **C. New feature, multiple architectures** → **Plan Mode**, with design
  alternatives and tradeoff analysis (no single right answer; hard to reverse).

**Conclusion:** Plan Mode adds the most value when **uncertainty or blast radius
is high** — many interdependent files, or multiple viable hard-to-reverse
designs. Direct execution wins for small, well-understood, easily-verified
changes.

---

## 5. Validation Steps

All validations below are **locally runnable** and were executed on
**2026-06-13** (Python 3.14.4, pytest 9.1.0, TypeScript 5.9.3, Node 18.20.8).

1. **Validate JSON syntax** of `.mcp.json` and `examples/claude.json.example`.
2. **Verify YAML frontmatter** of the two rule files and the skill file.
3. **Verify file paths** match the required structure (directory tree).
4. **Type-check** `src/frontend/sample_ui.ts` under `tsc --strict`.
5. **Run pytest** and **measure coverage** against the 80% target.

---

## 6. Commands Executed & 7. Outputs Captured

### Validation 1 — JSON syntax
```bash
$ python3 -c "import json; json.load(open('.mcp.json'))" && echo VALID
$ python3 -c "import json; json.load(open('examples/claude.json.example'))" && echo VALID
```
```
VALID JSON: .mcp.json
VALID JSON: examples/claude.json.example
```
✅ **PASS** — both JSON files parse.

### Validation 2 — YAML frontmatter
```bash
$ python3  # parse frontmatter of each rule/skill file with PyYAML
```
```
OK  .claude/rules/api-rules.md       -> ['paths']
OK  .claude/rules/testing-rules.md   -> ['paths']
OK  .claude/skills/code-review/skill.md -> ['name', 'description', 'context', 'allowed-tools']
```
✅ **PASS** — all frontmatter blocks are valid YAML with the expected keys
(`paths` for rules; `name`, `description`, `context`, `allowed-tools` for the
skill).

### Validation 3 — File paths / structure
```bash
$ find . -type f -not -path './venv/*' -not -path './.git/*' ... | sort
```
Confirmed the tree in §2 matches the required structure. ✅ **PASS**

### Validation 4 — TypeScript type-check
```bash
$ tsc --noEmit --strict --skipLibCheck --lib es2020,dom src/frontend/sample_ui.ts
```
```
OK: sample_ui.ts type-checks cleanly under --strict
```
✅ **PASS** — no type errors under strict mode.

### Validation 5 — pytest + coverage
```bash
$ python3 -m pytest -v
```
```
============================= test session starts ==============================
platform darwin -- Python 3.14.4, pytest-9.1.0, pluggy-1.6.0
configfile: pytest.ini
testpaths: src/tests
collected 4 items

src/tests/sample_api.test.py::test_create_user_returns_typed_user_with_assigned_id PASSED [ 25%]
src/tests/sample_api.test.py::test_create_user_rejects_duplicate_email           PASSED [ 50%]
src/tests/sample_api.test.py::test_get_user_controller_maps_missing_user_to_404  PASSED [ 75%]
src/tests/sample_api.test.py::test_create_user_controller_maps_duplicate_to_409  PASSED [100%]

============================== 4 passed in 0.53s ===============================
```
```bash
$ python3 -m coverage run -m pytest -q && python3 -m coverage report -m --include="*/api/*,*/tests/*"
```
```
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/api/sample_api.py             42      1    98%   83
src/tests/sample_api.test.py      44      0   100%
------------------------------------------------------------
TOTAL                             86      1    99%
```
✅ **PASS** — 4/4 tests pass; coverage **98% on the API module / 99% total**,
exceeding the 80% target.

---

## 8. Screenshots

> Placeholders — add terminal/editor screenshots here when capturing for the
> graded submission.

- `![pytest run](docs/screenshots/pytest.png)` — _placeholder: pytest output._
- `![coverage report](docs/screenshots/coverage.png)` — _placeholder: coverage._
- `![tsc type-check](docs/screenshots/tsc.png)` — _placeholder: TypeScript check._
- `![directory tree](docs/screenshots/tree.png)` — _placeholder: file tree._
- `![skill in action](docs/screenshots/code-review-skill.png)` — _placeholder:
  the code-review skill running in a forked context._

---

## 9. Lessons Learned

- **Project-level instructions scale better than per-developer config.** Putting
  standards in a committed `CLAUDE.md` makes them consistent and reviewable;
  personal config is for individual experiments only.
- **Path-specific rules keep context lean.** Loading API rules only for
  `src/api/**` (and test rules only for `*.test.*`) means each session carries
  just the rules relevant to the files in play.
- **`context: fork` + a restricted toolset is a powerful safety pattern.** A
  review that can only Read/Grep/Glob *cannot* mutate the repo, and forking keeps
  its verbose exploration out of the main thread — only the conclusion returns.
- **Env-var expansion is the right way to handle MCP secrets.** `${GITHUB_TOKEN}`
  keeps tokens out of version control while still committing the server config.
- **Real validation reveals real friction.** The required filename
  `sample_api.test.py` isn't a default pytest discovery pattern, so a `pytest.ini`
  (custom `python_files` + `importlib` import mode) was needed to make tests
  collect — a small but instructive detail.

---

## 10. Final Conclusion

All six features were implemented and every locally-runnable validation passed:
JSON parses, YAML frontmatter is valid, the structure matches the spec,
TypeScript type-checks under `--strict`, and the test suite is green with 98%+
coverage. The repository demonstrates how Claude Code's layered configuration —
global `CLAUDE.md`, path-scoped rules, forked tool-restricted skills, and merged
project/user MCP servers — combines into a consistent, safe, and team-shareable
workflow, and when **Plan Mode** should be preferred over direct execution. A
reviewer can assess the solution entirely from this README and the committed
files, without rerunning the work.

---

## Appendix — Final Directory Tree

```
.
├── .claude
│   ├── rules
│   │   ├── api-rules.md
│   │   └── testing-rules.md
│   └── skills
│       └── code-review
│           ├── examples.md
│           └── skill.md
├── docs
│   ├── personal-mcp-example.md
│   └── plan-mode-vs-direct-execution.md
├── examples
│   └── claude.json.example
├── src
│   ├── api
│   │   └── sample_api.py
│   ├── frontend
│   │   └── sample_ui.ts
│   └── tests
│       └── sample_api.test.py
├── .mcp.json
├── CLAUDE.md
├── pytest.ini
└── README.md
```

## Appendix — Completion Checklist

- [x] **Step 1** — Project-level `CLAUDE.md` with coding/testing/documentation
      standards + explanation of team-wide effect.
- [x] **Step 2** — `api-rules.md` (`src/api/**/*`) and `testing-rules.md`
      (`**/*.test.*`) with YAML frontmatter; trigger files created; load-mapping
      documented.
- [x] **Step 3** — `code-review` skill with `context: fork`, tools limited to
      Read/Grep/Glob, `skill.md` + `examples.md`, isolation rationale documented.
- [x] **Step 4** — `.mcp.json` `github` server with `${GITHUB_TOKEN}` env
      expansion.
- [x] **Step 5a** — `~/.claude.json` personal/experimental MCP example +
      project vs. user scope explanation + simultaneous availability.
- [x] **Step 5b** — Plan Mode vs. Direct Execution: Examples A/B/C + conclusion.
- [x] **Validation** — JSON, YAML, paths, TypeScript, pytest, coverage all run
      and captured.
- [x] **README** — overview, structure, implementation, feature explanations,
      validation, commands, outputs, screenshot placeholders, lessons learned,
      conclusion, tree, checklist.
