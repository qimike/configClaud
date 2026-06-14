---
name: code-review
description: >-
  Perform a structured code review of the current changes or a specified file
  set. Identifies bugs, suggests improvements, and reports security findings.
  Use when the user asks for a code review, a bug hunt, or a security pass.
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Code Review Skill (project-scoped)

This is a **project-scoped** skill: it lives in `.claude/skills/` inside this
repository, so it is available to anyone who clones the repo and is
version-controlled alongside the code it reviews.

## What this skill does

When invoked, perform a thorough, read-only review of the relevant code and
produce a report with four sections:

1. **Summary** — what was reviewed and the overall assessment.
2. **Bugs** — concrete correctness defects, each with `file:line` and an
   explanation of how it fails.
3. **Improvements** — refactors, simplifications, and adherence to the project
   standards in `CLAUDE.md` (type hints, <50-line functions, composition,
   structured logging, no hardcoded secrets).
4. **Security findings** — hardcoded secrets, missing input validation,
   injection risks, unsafe deserialization, etc. Note severity for each.

## How to run the review

1. Use **Glob** to enumerate the files in scope (e.g. `src/api/**/*.py`).
2. Use **Read** to read each file in scope.
3. Use **Grep** to find risky patterns across the codebase (e.g.
   `password`, `token`, `eval(`, `pickle.loads`, `verify=False`).
4. Cross-check findings against `CLAUDE.md` and `.claude/rules/`.
5. Emit the four-section report. Do **not** modify any files.

See `examples.md` for a worked example of the expected output.

## Tooling restriction

This skill is restricted to **Read**, **Grep**, and **Glob** only. It cannot
edit files, run shell commands, or make network calls. A review should *observe*,
not *change* — limiting the toolset makes that guarantee enforceable rather than
a matter of trust.

## Why context isolation (`context: fork`) is useful

`context: fork` runs the skill in a **forked (isolated) sub-context**:

- **It avoids polluting the main conversation context.** A review reads many
  files and produces a lot of intermediate text. Without isolation, all of that
  would accumulate in the main thread, crowding out the task the user actually
  cares about and burning the context window.
- **Only the final report returns to the main conversation.** The forked context
  does the noisy work — reading files, grepping, reasoning over each finding —
  and hands back just the structured summary. The main thread stays focused and
  small.
- **It keeps reviews reproducible and side-effect free.** Combined with the
  Read/Grep/Glob-only tool restriction, the fork can explore freely with no risk
  of altering the working tree or leaking review scaffolding into later turns.

In short: **fork = do the heavy reading elsewhere, return only the conclusion.**
