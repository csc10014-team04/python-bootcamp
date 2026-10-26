"""I/O utilities for loading and saving tasks."""

import csv
import json
from datetime import datetime
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Load study tasks from a CSV file.

    Args:
        path: Path to the CSV file.

    Returns:
        List of parsed Task objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a row contains invalid or missing data.
    """
    tasks: list[Task] = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_num, row in enumerate(reader, start=2):
            try:
                tasks.append(
                    Task(
                        title=row["title"],
                        importance=int(row["importance"]),
                        effort_h=float(row["effort_h"]),
                        deadline=datetime.strptime(row["deadline"], "%Y-%m-%d").date(),
                    )
                )
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Invalid row at line {line_num}: {exc}") from exc
    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Save a list of tasks to a JSON file.

    Args:
        tasks: List of Task instances to serialize.
        path: Target file path.
    """
    data = [
        {
            "title": t.title,
            "importance": t.importance,
            "effort_h": t.effort_h,
            "deadline": t.deadline.isoformat(),
        }
        for t in tasks
    ]

    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
