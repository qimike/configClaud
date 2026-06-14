# Code Review Skill — Examples

A worked example of the output the `code-review` skill should produce. The input
below is a deliberately flawed snippet; the report shows the expected structure.

## Example input (hypothetical `src/api/payments.py`)

```python
import sqlite3

API_KEY = "sk_live_51H8xQ: hardcoded"  # secret committed to source

def charge(user_input):
    db = sqlite3.connect("app.db")
    # builds SQL by string concatenation
    db.execute("SELECT * FROM cards WHERE owner = '" + user_input + "'")
    return db.fetchall()
```

## Example output

### 1. Summary
Reviewed `src/api/payments.py` (1 function, 8 lines). The file has one critical
security issue, one high-severity injection risk, and several deviations from the
project standards in `CLAUDE.md`.

### 2. Bugs
- **`src/api/payments.py:9` — `fetchall` called on the connection, not a cursor.**
  `sqlite3.Connection.execute` returns a cursor; `db.fetchall()` will raise
  `AttributeError` at runtime. Use `cursor = db.execute(...); cursor.fetchall()`.

### 3. Improvements
- **Missing type hints** (`CLAUDE.md` → Coding Standards). `charge(user_input)`
  should be `charge(user_input: str) -> list[Row]`.
- **No docstring** on a public function (`CLAUDE.md` → Documentation Standards).
- **No input validation** (`api-rules.md`). Validate `user_input` with a Pydantic
  model before use.
- **Business logic in a would-be controller** (`api-rules.md`). Move DB access to
  a service layer.

### 4. Security findings
- **CRITICAL — Hardcoded secret (`src/api/payments.py:3`).** `API_KEY` is a live
  key committed to source. Remove it, rotate the key, and load it from an
  environment variable (`CLAUDE.md` → "Avoid hardcoded secrets").
- **HIGH — SQL injection (`src/api/payments.py:8`).** User input is concatenated
  into the query. Use parameterized queries:
  `db.execute("SELECT * FROM cards WHERE owner = ?", (user_input,))`.

---

## How to invoke

```
/code-review
```

Or ask in natural language: *"Run a code review on `src/api/`."* The skill runs in
a forked context with Read/Grep/Glob only, and returns just this report.
