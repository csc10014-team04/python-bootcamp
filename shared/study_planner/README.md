# Study Planner (`shared.study_planner`)

The `study_planner` package provides a CLI tool and reusable Python pipeline to parse, prioritise, allocate, and render daily study schedules from CSV task lists.

---

## Architecture & Pipeline

The system is decomposed into decoupled, single-responsibility modules:

```mermaid
flowchart LR
    A["CSV File"] --> B["io.parse_csv"]
    B -->|list[Task]| C["prioritise.prioritise"]
    C -->|sorted tasks| D["allocate.allocate"]
    D -->|selected tasks| E["render.render"]
    E --> F["Printable Schedule"]
```

### Module Overview

| Module | Responsibility | Key Exports |
| :--- | :--- | :--- |
| [`models.py`](models.py) | Domain model and field validation. | `Task` |
| [`io.py`](io.py) | CSV ingestion and natural language deadline parsing. | `parse_csv`, `parse_due` |
| [`prioritise.py`](prioritise.py) | Active task filtering and strategy-based sorting. | `prioritise` |
| [`allocate.py`](allocate.py) | Greedy capacity allocation within available hours. | `allocate` |
| [`render.py`](render.py) | Formatted ASCII schedule generation with dots alignment. | `render` |
| [`errors.py`](errors.py) | Exception hierarchy for domain and file errors. | `StudyPlannerError`, `EmptyFileError`, `InfeasiblePlan` |
| [`__main__.py`](__main__.py) | CLI entry point and pipeline coordination. | `run_pipeline`, `main` |

---

## CSV File Specification

The planner requires a comma-separated values (CSV) file with exactly 4 columns:

| Column | Type | Constraints / Format | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | Non-empty string | The title or description of the task. |
| `importance` | `int` | `1` to `5` (`5` is highest) | Priority score. |
| `effort_h` | `float` | Non-negative (`>= 0.0`) | Estimated effort required in hours. |
| `deadline` | `str` | ISO or relative format | Target completion date. |

### Deadline Formats

- **Relative terms:** `today`, `tomorrow`, `in <N> days` (e.g. `in 2 days`, `in 5 days`)
- **Weekdays:** `mon`, `monday`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun` (resolves to the upcoming occurrence)
- **ISO dates:** `YYYY-MM-DD` (e.g. `2026-11-05`)

---

## CLI Usage

Run the module using Python's `-m` switch:

```bash
python -m shared.study_planner <file> --hours <hours> [options]
```

### Positional Arguments

- `file`: Path to the CSV task list file.

### Options and Flags

- `--hours <FLOAT>` (**required**): Total available study hours tonight (must be non-negative).
- `--today <YYYY-MM-DD>` (*optional*): Anchor date used for calculating relative deadlines (defaults to today's date).
- `--strategy {deadline,importance}` (*optional*): Sorting strategy (defaults to `deadline`).
  - `deadline`: Sorts earliest deadline first, tie-breaking by higher importance, then task title.
  - `importance`: Sorts highest importance first, tie-breaking by earliest deadline, then task title.

---

## Examples

### 1. Normal Schedule

Given `samples/tasks.csv`:
```csv
title,importance,effort_h,deadline
Assignment,4,1.5,tomorrow
DS exam,5,0.5,in 2 days
OS project,3,3.0,in 5 days
```

Command:
```bash
python -m shared.study_planner samples/tasks.csv --hours 2
```

Output:
```text
Tonight (2.0 h):
 1. Assignment ...... 1.5 h
 2. DS exam ......... 0.5 h
```

### 2. Prioritise by Importance

Command:
```bash
python -m shared.study_planner samples/tasks.csv --hours 4 --strategy importance
```

Output:
```text
Tonight (4.0 h):
 1. DS exam ......... 0.5 h
 2. Assignment ...... 1.5 h
```

---

## Error Handling & Exit Codes

The CLI returns standard exit codes:
- `0`: Execution succeeded and schedule was output to `stdout`.
- `1`: Validation, parsing, or runtime error (error message emitted to `stderr`).

### Error Conditions Handled

- **File Not Found:** File does not exist at the specified path (`FileNotFoundError`).
- **Empty File:** 0-byte file or file with header only (`EmptyFileError`).
- **Negative Hours:** Providing `--hours` less than 0.
- **Malformed CSV:** Missing columns, invalid importance ranges, negative effort, or unparseable deadlines.
- **Infeasible Plan:** Raised when tasks cannot fit or exceed the planned threshold.
