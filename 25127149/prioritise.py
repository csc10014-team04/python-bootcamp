"""Prioritise study tasks before allocating time to them."""

from datetime import date
from typing import Protocol


class Task(Protocol):
    """Describe the task attributes required by the prioritisation engine."""

    title: str
    importance: int
    deadline: date


def prioritise(
    tasks: list[Task],
    today: date,
    strategy: str = "deadline",
) -> list[Task]:
    """Filter expired tasks and return a new list sorted by the selected strategy.

    Args:
        tasks: Tasks to consider. The original list is not modified.
        today: Reference date; tasks with deadlines before this date are expired.
        strategy: Either ``"deadline"`` or ``"importance"``.

    Returns:
        A new list of non-expired tasks in priority order.

    Raises:
        ValueError: If ``strategy`` is not ``"deadline"`` or ``"importance"``.
    """
    if strategy not in {"deadline", "importance"}:
        raise ValueError(
            f"Unknown strategy {strategy!r}; expected 'deadline' or 'importance'."
        )

    active_tasks = [task for task in tasks if task.deadline >= today]

    if strategy == "deadline":
        return sorted(
            active_tasks,
            key=lambda task: (task.deadline, -task.importance, task.title),
        )

    return sorted(
        active_tasks,
        key=lambda task: (-task.importance, task.deadline, task.title),
    )
