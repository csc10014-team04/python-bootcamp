
"""Capacity allocation and time budget planning."""

from .errors import InfeasiblePlan
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
        InfeasiblePlan: If a task cannot fit within the remaining hours.
    """
    if hours < 0:
        raise ValueError("Available hours must be non-negative")

    selected: list[Task] = []
    remaining = hours

    for task in tasks:
        if task.effort_h <= remaining:
            selected.append(task)
            remaining -= task.effort_h
        else:
            needed_h = sum(t.effort_h for t in selected) + task.effort_h
            raise InfeasiblePlan(needed_h, hours)

    return selected
