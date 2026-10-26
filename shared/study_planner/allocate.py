"""Capacity allocation and time budget planning."""

from .models import Task


def allocate(tasks: list[Task], hours: float) -> list[Task]:
    """Allocate available hours to prioritised tasks greedily.

    Args:
        tasks: Prioritised candidate tasks.
        hours: Available study hours tonight.

    Returns:
        List of selected tasks that fit within the given time budget.

    Raises:
        ValueError: If available hours is negative.
    """
    if hours < 0:
        raise ValueError("Available hours must be non-negative")

    selected: list[Task] = []
    remaining = hours

    for task in tasks:
        if task.effort_h <= remaining:
            selected.append(task)
            remaining -= task.effort_h
            if remaining <= 0:
                break

    return selected

