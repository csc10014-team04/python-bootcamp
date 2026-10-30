"""Load task records from CSV and save them as JSON."""

import csv
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any

from w2.w2_1 import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Load and validate tasks from a CSV file.

    The CSV header must be title,importance,effort_h,deadline.
    """
    tasks: list[Task] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        expected = ["title", "importance", "effort_h", "deadline"]
        if reader.fieldnames != expected:
            raise ValueError(
                "CSV header must be: title,importance,effort_h,deadline"
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                task = Task(
                    title=row["title"].strip(),
                    importance=int(row["importance"]),
                    effort_h=float(row["effort_h"]),
                    deadline=date.fromisoformat(row["deadline"].strip()),
                )
                tasks.append(task)
            except (ValueError, TypeError, AttributeError, KeyError) as error:
                raise ValueError(
                    f"Invalid data at line {line_number}: {error}"
                ) from error
    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Serialize tasks to a UTF-8 JSON file."""
    data: list[dict[str, Any]] = []
    for task in tasks:
        item = asdict(task)
        item["deadline"] = task.deadline.isoformat()
        data.append(item)

    with Path(path).open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
