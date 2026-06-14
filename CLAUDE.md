# CLAUDE.md — Project Instructions

This file is loaded automatically by Claude Code for **every** session opened in
this repository. It sets the baseline standards that apply to all developers and
all AI-assisted work, regardless of who is working or which files they touch.

> **How project-level instructions affect all developers**
> Anything written here is injected into Claude Code's context at the start of
> each session for this project. It is *shared* and version-controlled, so every
> teammate — and every Claude Code run — operates under the same rules. Unlike a
> personal `~/.claude/CLAUDE.md` (which only affects one machine), this file
> guarantees consistency: code review, generation, and refactoring all follow the
> same conventions. Updating this file updates the rules for the whole team in one
> commit.

---

## Coding Standards

- **Python type hints are required** on all function signatures and return types.
- **Functions should stay under 50 lines.** Extract helpers when they grow.
- **Prefer composition over inheritance.** Inject collaborators; avoid deep class
  hierarchies.
- **Use structured logging** (key=value or JSON), never bare `print` statements.
- **Avoid hardcoded secrets.** Read credentials from environment variables or a
  secrets manager — never commit tokens, keys, or passwords.

## Testing Standards

- **Unit tests are required for every new feature.**
- **Minimum test coverage target: 80%.**
- **Use `pytest`** as the test runner.

## Documentation Standards

- **Public functions require docstrings** describing args, returns, and raised
  errors.
- **Complex logic requires inline comments** explaining the *why*, not the *what*.

---

## Scope of these rules

These standards are global to the project. More specific, path-scoped rules live
in `.claude/rules/` and apply only when matching files are in context:

- `.claude/rules/api-rules.md` → applies to `src/api/**/*`
- `.claude/rules/testing-rules.md` → applies to `**/*.test.*`

When a path-specific rule and this file overlap, treat the path-specific rule as
an addition/refinement, not a replacement, of these baseline standards.
