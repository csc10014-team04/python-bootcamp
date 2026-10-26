"""Task prioritisation engine."""

from datetime import date

from .models import Task


def prioritise(
    tasks: list[Task], today: date, strategy: str = "deadline"
) -> list[Task]:
    """Order study tasks by urgency and importance.

    Filters out tasks that are already overdue (deadline < today).

    Args:
        tasks: Candidate tasks to prioritise.
        today: Anchor date for relative comparisons.
        strategy: Sort strategy, either "deadline" or "importance".

    Returns:
        Sorted list of active tasks.
    """
    active = [t for t in tasks if t.deadline >= today]

    if strategy == "importance":
        return sorted(active, key=lambda t: (-t.importance, t.deadline, t.title))

    # Default "deadline" strategy: earliest deadline first, then highest importance, then title
    return sorted(active, key=lambda t: (t.deadline, -t.importance, t.title))

