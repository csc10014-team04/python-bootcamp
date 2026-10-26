"""Unit tests for Week 3 implementations."""

import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import pytest

from W2.models import Task
from w3.cli import format_schedule, select_tasks
from w3.dates import parse_due
from w3.log_stats import analyse


# --- W3-1 Tests ---
def test_parse_due_iso() -> None:
    """Test parsing standard ISO YYYY-MM-DD date strings."""
    today = date(2026, 10, 26)
    assert parse_due("2026-10-30", today) == date(2026, 10, 30)
    assert parse_due(" 2026-12-25  ", today) == date(2026, 12, 25)


def test_parse_due_tomorrow() -> None:
    """Test parsing 'tomorrow' relative to today."""
    today = date(2026, 10, 26)
    assert parse_due("tomorrow", today) == date(2026, 10, 27)
    assert parse_due(" TOMORROW ", today) == date(2026, 10, 27)


def test_parse_due_in_days() -> None:
    """Test parsing relative offsets like 'in N days'."""
    today = date(2026, 10, 26)
    assert parse_due("in 3 days", today) == date(2026, 10, 29)
    assert parse_due("in 1 day", today) == date(2026, 10, 27)
    assert parse_due("in 0 days", today) == date(2026, 10, 26)


def test_parse_due_weekdays_next_occurrence() -> None:
    """Test parsing weekday names and finding the next occurrence (1-7 days away)."""
    # 2026-10-26 is Monday (weekday 0)
    today = date(2026, 10, 26)
    assert parse_due("Tue", today) == date(2026, 10, 27)
    assert parse_due("Tuesday", today) == date(2026, 10, 27)
    assert parse_due("Fri", today) == date(2026, 10, 30)
    assert parse_due("Friday", today) == date(2026, 10, 30)
    # Asking for "Mon" when today is Monday must return next week's Monday (+7 days)
    assert parse_due("Mon", today) == date(2026, 11, 2)
    assert parse_due("Monday", today) == date(2026, 11, 2)

    # Test Friday anchor (2026-10-30, weekday 4)
    friday = date(2026, 10, 30)
    assert parse_due("Fri", friday) == date(2026, 11, 6)
    assert parse_due("Sat", friday) == date(2026, 10, 31)
    assert parse_due("Sun", friday) == date(2026, 11, 1)


def test_parse_due_unknown() -> None:
    """Test that unrecognized or invalid date strings raise ValueError."""
    today = date(2026, 10, 26)
    with pytest.raises(ValueError):
        parse_due("invalid date", today)
    with pytest.raises(ValueError):
        parse_due("yesterday", today)
    with pytest.raises(ValueError):
        parse_due("2026-02-31", today)
    with pytest.raises(ValueError):
        parse_due("", today)


# --- W3-2 Tests ---
def test_analyse_empty() -> None:
    """Test log analysis with an empty input list."""
    res = analyse([])
    assert res == {
        "counts": Counter(),
        "p95": {},
        "slowest": None,
    }


def test_analyse_normal() -> None:
    """Test log analysis with multiple routes and latencies."""
    pairs = [
        ("/home", 10.0),
        ("/home", 20.0),
        ("/api/chat", 100.0),
        ("/api/chat", 200.0),
        ("/api/chat", 50.0),
        ("/api/chat", 300.0),
    ]
    res = analyse(pairs)
    assert res["counts"]["/home"] == 2
    assert res["counts"]["/api/chat"] == 4
    # /home: [10.0, 20.0], p95 index: ceil(0.95*2)-1 = 2-1 = 1 -> 20.0
    assert res["p95"]["/home"] == 20.0
    # /api/chat: [50.0, 100.0, 200.0, 300.0], ceil(0.95*4)-1 = 4-1 = 3 -> 300.0
    assert res["p95"]["/api/chat"] == 300.0
    assert res["slowest"] == "/api/chat"


def test_analyse_single_pair() -> None:
    """Test log analysis with a single request."""
    res = analyse([("/status", 42.0)])
    assert res["counts"]["/status"] == 1
    assert res["p95"]["/status"] == 42.0
    assert res["slowest"] == "/status"


# --- W3-3 Tests ---
def test_select_tasks_and_format_schedule() -> None:
    """Test selecting tasks within available hours and formatting the tonight summary."""
    today = date(2026, 10, 26)
    tasks = [
        Task(
            title="Assignment", importance=4, effort_h=1.5, deadline=date(2026, 10, 27)
        ),
        Task(title="DS exam", importance=5, effort_h=0.5, deadline=date(2026, 10, 28)),
        Task(title="Old task", importance=2, effort_h=1.0, deadline=date(2026, 10, 20)),
        Task(
            title="Heavy project",
            importance=5,
            effort_h=5.0,
            deadline=date(2026, 10, 29),
        ),
    ]
    selected = select_tasks(tasks, hours=2.0, today=today)
    assert len(selected) == 2
    assert selected[0].title == "Assignment"
    assert selected[1].title == "DS exam"

    formatted = format_schedule(selected, hours=2.0)
    expected = (
        "Tonight (2.0 h):\n 1. Assignment ...... 1.5 h\n 2. DS exam ......... 0.5 h"
    )
    assert formatted == expected


def test_cli_subprocess_missing_file() -> None:
    """Test CLI exit code and error output when the task file does not exist."""
    cli_path = Path(__file__).resolve().parent / "cli.py"
    res = subprocess.run(
        [sys.executable, str(cli_path), "non_existent.csv", "--hours", "2"],
        capture_output=True,
        check=False,
        text=True,
    )
    assert res.returncode == 1
    assert "file not found" in res.stderr.lower()


def test_cli_subprocess_success(tmp_path: Path) -> None:
    """Test CLI execution with a valid CSV file."""
    csv_file = tmp_path / "sample_tasks.csv"
    csv_file.write_text(
        "title,importance,effort_h,deadline\n"
        "Assignment,4,1.5,2026-10-27\n"
        "DS exam,5,0.5,2026-10-28\n",
        encoding="utf-8",
    )
    cli_path = Path(__file__).resolve().parent / "cli.py"
    res = subprocess.run(
        [
            sys.executable,
            str(cli_path),
            str(csv_file),
            "--hours",
            "2",
            "--today",
            "2026-10-26",
        ],
        capture_output=True,
        check=False,
        text=True,
    )
    assert res.returncode == 0
    assert "Tonight (2.0 h):" in res.stdout
    assert " 1. Assignment ...... 1.5 h" in res.stdout
    assert " 2. DS exam ......... 0.5 h" in res.stdout
