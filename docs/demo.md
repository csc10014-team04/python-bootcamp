# Study Planner End-to-End Demo

This document demonstrates the functionality, edge cases, error handling, and test execution for the `shared.study_planner` command-line application.

---

## 1. Datasets

### Sample 1: Standard Tasks (`samples/tasks.csv`)
```csv
title,importance,effort_h,deadline
Assignment,4,1.5,tomorrow
DS exam,5,0.5,in 2 days
OS project,3,3.0,in 5 days
```

### Sample 2: Empty CSV (`samples/empty.csv`)
```csv
title,importance,effort_h,deadline
```

### Sample 3: Infeasible Plan (`samples/infeasible.csv`)
```csv
title,importance,effort_h,deadline
Comprehensive Exam,5,10.0,tomorrow
```

---

## 2. Command Scenarios and Real Output

### Scenario 1: Standard Execution (2 Hours Available)

**Command:**
```bash
python -m shared.study_planner samples/tasks.csv --hours 2
```

**Expected Exit Code:** `0`

**Terminal Output:**
```text
Tonight (2.0 h):
 1. Assignment ...... 1.5 h
 2. DS exam ......... 0.5 h
```
*Note: "OS project" requires 3.0 hours and exceeds the remaining budget tonight, so it is deferred.*

---

### Scenario 2: Extended Budget (5 Hours Available)

**Command:**
```bash
python -m shared.study_planner samples/tasks.csv --hours 5
```

**Expected Exit Code:** `0`

**Terminal Output:**
```text
Tonight (5.0 h):
 1. Assignment ...... 1.5 h
 2. DS exam ......... 0.5 h
 3. OS project ...... 3.0 h
```

---

### Scenario 3: Prioritising by Importance

**Command:**
```bash
python -m shared.study_planner samples/tasks.csv --hours 2 --strategy importance
```

**Expected Exit Code:** `0`

**Terminal Output:**
```text
Tonight (2.0 h):
 1. DS exam ......... 0.5 h
 2. Assignment ...... 1.5 h
```
*Note: "DS exam" has importance 5 and is scheduled before "Assignment" (importance 4).*

---

### Scenario 4: Anchoring with a Specific Date (`--today`)

**Command:**
```bash
python -m shared.study_planner samples/tasks.csv --hours 2 --today 2026-10-29
```

**Expected Exit Code:** `0`

**Terminal Output:**
```text
Tonight (2.0 h):
 1. Assignment ...... 1.5 h
 2. DS exam ......... 0.5 h
```

---

### Scenario 5: Missing File Error Handling

**Command:**
```bash
python -m shared.study_planner samples/nonexistent.csv --hours 2
```

**Expected Exit Code:** `1`

**Stderr Output:**
```text
Error: file not found: samples/nonexistent.csv
```

---

### Scenario 6: Empty File Error Handling

**Command:**
```bash
python -m shared.study_planner samples/empty.csv --hours 2
```

**Expected Exit Code:** `1`

**Stderr Output:**
```text
Error: empty file: csv file contains header only with no records
```

---

### Scenario 7: Negative Hours Error Handling

**Command:**
```bash
python -m shared.study_planner samples/tasks.csv --hours -1
```

**Expected Exit Code:** `1`

**Stderr Output:**
```text
Error: --hours must be non-negative
```

---

### Scenario 8: Infeasible Plan Dataset

**Command:**
```bash
python -m shared.study_planner samples/infeasible.csv --hours 1
```

**Expected Exit Code:** `0`

**Terminal Output:**
```text
Tonight (1.0 h):
No tasks fit the available time.
```

---

## 3. Automated Test Suite Execution

All test cases are verified via end-to-end integration tests using `pytest` and `subprocess.run`:

```bash
pytest tests/test_study_planner_e2e.py -v
```

**Output:**
```text
============================= test session starts =============================
platform win32 -- Python 3.14.8, pytest-9.1.1, pluggy-1.7.0
rootdir: python-bootcamp
configfile: pyproject.toml
testpaths: tests
collected 7 items

tests/test_study_planner_e2e.py::test_normal_execution PASSED            [ 14%]
tests/test_study_planner_e2e.py::test_missing_file_error PASSED          [ 28%]
tests/test_study_planner_e2e.py::test_empty_file_error PASSED            [ 42%]
tests/test_study_planner_e2e.py::test_zero_byte_empty_file_error PASSED  [ 57%]
tests/test_study_planner_e2e.py::test_negative_hours_error PASSED        [ 71%]
tests/test_study_planner_e2e.py::test_infeasible_plan_dataset PASSED     [ 85%]
tests/test_study_planner_e2e.py::test_custom_today_and_importance_strategy PASSED [100%]

============================== 7 passed in 0.99s ==============================
```

---

## 4. Code Quality & Linting

Run `ruff` to ensure compliance with PEP 8 and project style guidelines:

```bash
ruff check .
```

**Output:**
```text
All checks passed!
```
