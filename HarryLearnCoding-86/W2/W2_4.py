"""Week 2 Task 4: Filter urgent tasks unit tests."""

from typing import Any


def filter_urgent_tasks(
    tasks: list[dict[str, Any]], threshold: float
) -> list[dict[str, Any]]:
    """Filter tasks whose effort does not exceed the given threshold.

    Args:
        tasks: List of task dictionaries containing an effort field.
        threshold: Maximum allowed effort.

    Returns:
        Filtered list of task dictionaries.

    Raises:
        ValueError: If threshold is negative.
    """
    if threshold < 0:
        raise ValueError("Threshold cannot be negative")
    return [t for t in tasks if t.get("effort_h", t.get("effort", 0.0)) <= threshold]


def test_filter_all_exceed() -> None:
    """Test that all tasks exceeding threshold are filtered out."""
    tasks = [
        {"title": "Task A", "effort_h": 10.0},
        {"title": "Task B", "effort_h": 7.5},
    ]
    assert filter_urgent_tasks(tasks, 5.0) == []
