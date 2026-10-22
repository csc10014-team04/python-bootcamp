from datetime import date
from typing import Any
from .models import Task

REQUIRED_KEYS = {"title", "importance", "effort_h", "deadline"}

def task_from_dict(data: dict[str, Any]) -> Task:
    """Parses a dictionary into a Task, validating structural integrity.

    Raises KeyError if any required keys are missing.
    """
    missing_keys = REQUIRED_KEYS - data.keys()
    if missing_keys:
        raise KeyError(
            f"Input dictionary is missing required key(s): {', '.join(sorted(missing_keys))}"
        )

    return Task(
        title=data["title"],
        importance=data["importance"],
        effort_h=data["effort_h"],
        deadline=data["deadline"],
    )