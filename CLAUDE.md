# CLAUDE.md — AI Assistant Guide for PythonToDo

## Project Overview

PythonToDo is a command-line to-do list application that automatically prioritizes tasks using
a **Weighted Shortest Remaining Time (WSRT)** scheduling algorithm, inspired by the book
*Algorithms to Live By* by Brian Christian & Tom Griffiths. The core formula is:

```
Priority Score = Importance / Effort
```

Tasks with a higher score are surfaced first. It is a **learning project** — expect rough edges,
missing features, and known bugs.

---

## Repository Structure

```
/home/user/PythonToDo/
├── app.py              # Entire application (single file, ~190 lines)
├── todo_database.db    # SQLite database (tracked in git; auto-created on first run)
├── README.md           # Project description, algorithm notes, and roadmap
├── CLAUDE.md           # This file
├── .gitignore          # Standard Python gitignore
└── .vscode/
    └── settings.json   # VSCode: basic type-checking enabled
```

There is no `requirements.txt` — the only dependency is Python's standard library (`sqlite3`).

---

## Running the Application

```bash
python app.py
```

The app enters an interactive REPL loop. Supported commands:

| Command  | Description                                                  |
|----------|--------------------------------------------------------------|
| `add`    | Prompt for task, effort, importance, optional start/deadline |
| `list`   | Print all tasks raw (tuple format, unsorted)                 |
| `rank`   | Print the single highest-priority task                       |
| `edit`   | Select a task by ID and update individual fields             |
| `delete` | Select a task by ID and remove it                            |
| `exit`   | Quit the application                                         |

No CLI flags, arguments, or subcommands — all interaction is through stdin prompts.

---

## Architecture

All application logic lives in `app.py`. There is no package structure, no separate modules,
and no web framework.

### Module-level setup (lines 1–22)

```python
dbconnection = sqlite3.connect("todo_database.db")
dbcursor = dbconnection.cursor()
```

The database connection and cursor are **global singletons** created at import time. The
`todo_items` table is created if it does not exist.

### Database Schema

```sql
CREATE TABLE IF NOT EXISTS todo_items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task          TEXT,
    effort        INTEGER,
    importance    INTEGER,
    earliestStart DATE,
    deadline      DATE,
    score         REAL AS ( CAST(importance AS REAL) / effort ) STORED
);
```

`score` is a **SQLite generated column** — it is computed automatically and stored on disk.
It does not need to be inserted or updated manually.

### `ListItem` class (lines 28–158)

The class is used both as a data model and as a namespace for CRUD operations via
`@classmethod` methods. In practice, `ListItem` instances are appended to
`ListItem.instances` in `__init__` but that list is never read anywhere — CRUD
operations query the database directly instead.

| Member                 | Type         | Purpose                                     |
|------------------------|--------------|---------------------------------------------|
| `instances`            | class attr   | List of all `ListItem` objects (unused)     |
| `__init__`             | instance     | Set fields and append to `instances`        |
| `__str__`              | instance     | Human-readable summary                      |
| `add()`                | classmethod  | Prompt user, INSERT into DB                 |
| `list()`               | classmethod  | SELECT * and print raw tuples               |
| `edit()`               | classmethod  | SELECT, prompt for fields, UPDATE in DB     |
| `rank()`               | classmethod  | SELECT top-score row, print task name       |
| `delete()`             | classmethod  | SELECT, prompt for ID, DELETE from DB       |
| `task` / `effort` / `importance` | property | Getter + setter with falsy validation |

### `main()` function (lines 161–189)

A simple `while True` loop that reads user input and dispatches to the appropriate
`ListItem` classmethod. Unknown commands reset silently (no error message).

---

## Code Conventions

- **Formatting:** Black (applied as of Nov 2023 commit).
- **Naming:**
  - Classes → `PascalCase` (`ListItem`)
  - Methods, functions, local variables → `snake_case`
  - Column names in DB → mixed (`earliestStart`, `deadline` are camelCase; others are lowercase)
- **SQL:** Always uses parameterized queries with `?` placeholders — never string interpolation.
- **Commits:** Use `.commit()` manually after every write operation (`INSERT`, `UPDATE`).
- **Type hints:** None used. Do not add them unless the user asks.
- **Docstrings:** None used. Do not add them unless the user asks.
- **Error handling:** None used throughout. Do not add it unless the user asks — keep changes minimal.

---

## Known Bugs and Limitations

These are existing issues in the codebase. **Do not fix them silently** — surface them to the
user and ask before changing behavior.

1. **`delete()` SQL bug (line 128):** `item_id` is passed as a bare string, not a tuple.
   SQLite iterates the string character-by-character, producing wrong results for multi-digit
   IDs. Fix: `(item_id,)`.

2. **`delete()` missing commit (line 128):** `dbconnection.commit()` is never called after
   `DELETE`, so deletions are not persisted across sessions.

3. **`ListItem.instances` is unused:** The class attribute is populated in `__init__` but
   never read by any CRUD method or by `main()`. All reads go directly to the database.

4. **`earliestStart` and `deadline` are not integrated:** The DB columns and the `add()`
   prompts exist, but `rank()` and `list()` make no use of them in scheduling logic.

5. **No input validation in `add()`:** `effort` and `importance` are cast to `int` without
   a try/except, so non-numeric input raises an unhandled `ValueError`.

6. **`list()` does not sort:** It performs `SELECT *` with no `ORDER BY`, so tasks are
   displayed in insertion order rather than priority order.

7. **Unknown commands fail silently:** In `main()`, an unrecognized command resets
   `command = ""` with no user feedback.

---

## Tests

**There are no tests.** There is no test runner configuration, no `pytest.ini`, no
`conftest.py`, and no test files. If adding tests, use `pytest` and place test files in
a `tests/` directory following the `test_*.py` naming convention.

---

## Development Workflow

### Branching

- `master` — main branch; reflects production-ready code
- Feature/AI branches use the pattern `claude/<description>-<id>`

### Making changes

1. Work on the designated branch (never push directly to `master` without permission).
2. Commit with clear, descriptive messages.
3. Push with `git push -u origin <branch-name>`.

### Running

No build step. No virtual environment is required (only stdlib used). Run directly:

```bash
python app.py
```

The database file `todo_database.db` is created in the current working directory on first
run and is tracked in git.

---

## Planned Features (from README)

These are aspirational — do not implement them unless explicitly requested:

- Deadline and earliest-start-date scheduling logic
- Default field values
- Precedence constraints (priority inheritance for blocked tasks)
- Task hierarchies / sub-tasks
- Calendar scheduling with daily time budget
- Multi-device / cloud sync

---

## AI Assistant Guidelines

- **Minimal changes by default.** This is a learning project. Prefer small, targeted edits
  over broad refactors. Do not rewrite working code to be "cleaner" unless asked.
- **Do not add docstrings, type hints, or comments** to code you did not change.
- **Do not add error handling** for cases the user has not encountered — keep the code simple.
- **Surface bugs before fixing them.** The known bugs above are pre-existing; ask the user
  before changing behavior.
- **Respect the design philosophy:** The app should "never tell users off." Features that
  punish or block users on bad input go against the project's intent.
- **Single-file architecture is intentional.** Do not split `app.py` into modules unless asked.
- **No new dependencies.** The stdlib-only approach is deliberate for simplicity.
