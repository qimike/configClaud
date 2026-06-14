# Plan Mode vs. Direct Execution

Claude Code can either **execute directly** (read, edit, run as it goes) or work in
**Plan Mode**, where it researches and proposes a written plan for approval before
touching any files. This document compares the two using three scenarios of
increasing complexity and concludes when Plan Mode adds the most value.

> **Rule of thumb:** the value of planning rises with *uncertainty* and *blast
> radius*. Low uncertainty + small blast radius → direct execution. High
> uncertainty or many interdependent files → Plan Mode.

---

## Example A — Single-file bug fix

**Scenario:** `get_user` returns a 500 instead of a 404 for a missing user in
`src/api/sample_api.py`.

### Direct execution workflow
1. Read `src/api/sample_api.py`.
2. Edit the `get_user` controller to catch `KeyError` and raise `HTTPException(404)`.
3. Run `pytest` to confirm the fix.

### Why planning is unnecessary
- The change is **localized to one function in one file**.
- The correct behaviour is **unambiguous** — there is one right answer.
- The blast radius is tiny and a test verifies it immediately. Writing a plan
  first would cost more than the fix itself.

**Verdict: Direct execution.**

---

## Example B — Multi-file library migration

**Scenario:** Migrate the project from Pydantic v1 to Pydantic v2 across all of
`src/`.

### Plan mode workflow
1. **Survey:** Grep for every Pydantic usage (`BaseModel`, `validator`,
   `.dict()`, `Config`, `Field`).
2. **Propose a plan** listing each affected file and the exact change.
3. Get approval, then execute file by file, running tests between batches.

### Dependency analysis
- `validator` → `field_validator`; `root_validator` → `model_validator`.
- `.dict()` / `.json()` → `.model_dump()` / `.model_dump_json()`.
- `class Config` → `model_config = ConfigDict(...)`.
- Shared models in `src/api/` are imported by `src/tests/` — both must move
  together or tests break.

### Migration checklist
- [ ] Inventory every Pydantic import and call site.
- [ ] Pin `pydantic>=2` in dependencies.
- [ ] Update models (`Config` → `model_config`).
- [ ] Update validators (`validator` → `field_validator`).
- [ ] Update serialization calls (`.dict()` → `.model_dump()`).
- [ ] Update tests that assert on serialized output.
- [ ] Run `pytest`; confirm 100% pass and coverage ≥ 80%.

### Why Plan Mode helps here
The change is **mechanical but wide** — many files, ordering matters, and a
half-finished migration leaves the repo broken. A plan makes the scope and order
explicit before any edit lands.

**Verdict: Plan Mode.**

---

## Example C — New feature with multiple possible architectures

**Scenario:** Add **persistent storage** to the API (today `UserService` is
in-memory).

### Plan mode workflow
1. Research how `UserService` is used and where persistence would plug in.
2. Present **design alternatives** with tradeoffs.
3. Let the user choose, then implement the selected design.

### Design alternatives
| Option | Description | Pros | Cons |
| --- | --- | --- | --- |
| **A. SQLite + raw SQL** | Add a thin SQL repository. | No ORM dependency; simple. | Manual SQL; more boilerplate. |
| **B. SQLAlchemy ORM** | Repository backed by an ORM. | Mature, migrations, relationships. | Heavier dependency; learning curve. |
| **C. Repository interface + pluggable backends** | Define a `UserRepository` protocol; in-memory and SQL implementations. | Testable, swappable, composition-friendly. | More upfront abstraction. |

### Tradeoff analysis
- Option C aligns best with `CLAUDE.md` ("prefer composition over inheritance")
  and keeps the existing in-memory implementation for tests.
- Option B is the right call if relational queries and migrations are expected
  soon; otherwise it is over-engineering.
- Option A is fastest to ship but hardest to evolve.

Because the options have **materially different long-term consequences** and
there is **no single correct answer**, the decision should be made *before*
writing code — exactly what Plan Mode is for.

**Verdict: Plan Mode.**

---

## Conclusion — when Plan Mode provides the most value

Plan Mode delivers the **most value** when a task has **high uncertainty or a
large/interdependent blast radius** — specifically when:

- The change spans **many files** and ordering matters (Example B), or
- There are **multiple viable architectures** with different long-term tradeoffs
  and the decision is hard to reverse (Example C).

Direct execution is best for **small, well-understood, easily-verified changes**
where a single correct answer exists (Example A). Planning such a change adds
overhead without reducing risk.

**Bottom line:** plan when the *cost of a wrong direction* exceeds the *cost of
writing the plan*. For one-line fixes it doesn't; for migrations and architectural
features it almost always does.
