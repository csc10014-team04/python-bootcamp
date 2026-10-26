"""I/O functions for loading and parsing study tasks."""

import csv
import re
from datetime import date, timedelta
from pathlib import Path

from .errors import EmptyFileError
from .models import Task

_WEEKDAYS: dict[str, int] = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tues": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thur": 3,
    "thurs": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


def _parse_deadline(text: str, anchor: date) -> date:
    """Parse a date string or relative deadline descriptor."""
    clean = text.strip().lower()
    if not clean:
        raise ValueError("Deadline string cannot be empty")

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", clean):
        return date.fromisoformat(clean)

    if clean == "tomorrow":
        return anchor + timedelta(days=1)

    match = re.fullmatch(r"in\s+(\d+)\s+days?", clean)
    if match:
        return anchor + timedelta(days=int(match.group(1)))

    if clean in _WEEKDAYS:
        diff = (_WEEKDAYS[clean] - anchor.weekday()) % 7
        return anchor + timedelta(days=diff if diff > 0 else 7)

    raise ValueError(f"Unrecognized deadline format: {text!r}")


def parse_csv(path: str | Path, today: date | None = None) -> list[Task]:
    """Parse study tasks from a CSV file.

    Args:
        path: Path to the tasks CSV file.
        today: Anchor date for relative deadlines (defaults to date.today()).

    Returns:
        List of parsed Task objects.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        EmptyFileError: If the file is empty or has no task rows.
        ValueError: If a row contains invalid or missing data.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    anchor = today or date.today()
    tasks: list[Task] = []

    with file_path.open(mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise EmptyFileError(f"File is empty: {path}")

        for line_num, row in enumerate(reader, start=2):
            # Skip empty lines
            if not row or not any(row.values()):
                continue
            try:
                title = (row.get("title") or "").strip()
                if not title:
                    raise ValueError("Task title is required")
                importance = int(row["importance"])
                effort_h = float(row["effort_h"])
                deadline_raw = row["deadline"]
                deadline = _parse_deadline(deadline_raw, anchor)

                tasks.append(
                    Task(
                        title=title,
                        importance=importance,
                        effort_h=effort_h,
                        deadline=deadline,
                    )
                )
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Invalid row at line {line_num}: {exc}") from exc

    if not tasks:
        raise EmptyFileError(f"No task records found in {path}")

    return tasks

