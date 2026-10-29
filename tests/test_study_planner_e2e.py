"""End-to-end integration tests for shared.study_planner CLI."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = REPO_ROOT / "samples"
TASKS_CSV = SAMPLES_DIR / "tasks.csv"
EMPTY_CSV = SAMPLES_DIR / "empty.csv"
INFEASIBLE_CSV = SAMPLES_DIR / "infeasible.csv"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Execute the study planner CLI module in a subprocess."""
    cmd = [sys.executable, "-m", "shared.study_planner", *args]
    return subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_normal_execution() -> None:
    """Test normal CLI execution with samples/tasks.csv and --hours 2."""
    result = run_cli(str(TASKS_CSV), "--hours", "2")
    assert result.returncode == 0
    assert "Tonight (2.0 h):" in result.stdout
    assert "Assignment" in result.stdout
    assert "1.5 h" in result.stdout
    assert "DS exam" in result.stdout
    assert "0.5 h" in result.stdout
    # OS project requires 3.0h and should not fit tonight
    assert "OS project" not in result.stdout


def test_missing_file_error() -> None:
    """Test CLI error handling when task CSV file is missing."""
    missing_file = SAMPLES_DIR / "nonexistent_tasks_file.csv"
    result = run_cli(str(missing_file), "--hours", "2")
    assert result.returncode == 1
    assert "file not found" in result.stderr.lower() or "error:" in result.stderr.lower()


def test_empty_file_error() -> None:
    """Test CLI error handling when task CSV file contains header only."""
    result = run_cli(str(EMPTY_CSV), "--hours", "2")
    assert result.returncode == 1
    assert "empty file" in result.stderr.lower() or "error:" in result.stderr.lower()


def test_zero_byte_empty_file_error(tmp_path: Path) -> None:
    """Test CLI error handling when task CSV file is 0 bytes."""
    zero_file = tmp_path / "zero_bytes.csv"
    zero_file.touch()
    result = run_cli(str(zero_file), "--hours", "2")
    assert result.returncode == 1
    assert "empty file" in result.stderr.lower() or "error:" in result.stderr.lower()


def test_negative_hours_error() -> None:
    """Test CLI error handling when --hours is negative."""
    result = run_cli(str(TASKS_CSV), "--hours", "-1")
    assert result.returncode == 1
    assert "non-negative" in result.stderr.lower() or "error:" in result.stderr.lower()


def test_infeasible_plan_dataset() -> None:
    """Test CLI output when task effort exceeds available hours."""
    result = run_cli(str(INFEASIBLE_CSV), "--hours", "1")
    assert result.returncode == 0
    assert "Tonight (1.0 h):" in result.stdout
    assert "No tasks fit the available time." in result.stdout


def test_custom_today_and_importance_strategy() -> None:
    """Test CLI with explicit anchor date and importance prioritisation strategy."""
    result = run_cli(
        str(TASKS_CSV),
        "--hours",
        "4",
        "--today",
        "2026-10-29",
        "--strategy",
        "importance",
    )
    assert result.returncode == 0
    assert "Tonight (4.0 h):" in result.stdout
    # Under importance strategy: DS exam (importance 5, 0.5h) should be first,
    # followed by Assignment (importance 4, 1.5h)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    task_lines = [line for line in lines if line[0].isdigit()]
    assert len(task_lines) >= 2
    assert "DS exam" in task_lines[0]
    assert "Assignment" in task_lines[1]
