import csv
import re
from datetime import date, timedelta
from pathlib import Path

from .models import Task

try:
    from .errors import EmptyFileError
except ImportError:
    class EmptyFileError(Exception): # fallback for standalone execution
        pass


def parse_due(text: str, today: date) -> date:
    """resolve human readable due strings and iso dates into date objects."""
    raw = text.strip() # trim whitespace
    lower = raw.lower()

    if lower == "today":
        return today # return current date
    if lower == "tomorrow":
        return today + timedelta(days=1) # return following date

    match_in_days = re.fullmatch(r"in\s+(\d+)\s+days?", lower)
    if match_in_days:
        offset = int(match_in_days.group(1)) # extract numeric offset
        return today + timedelta(days=offset)

    weekdays = {
        "mon": 0, "monday": 0,
        "tue": 1, "tuesday": 1,
        "wed": 2, "wednesday": 2,
        "thu": 3, "thursday": 3,
        "fri": 4, "friday": 4,
        "sat": 5, "saturday": 5,
        "sun": 6, "sunday": 6,
    }
    if lower in weekdays:
        target_idx = weekdays[lower]
        days_ahead = (target_idx - today.weekday()) % 7 # compute days ahead
        if days_ahead == 0:
            days_ahead = 7 # step forward to next cycle
        return today + timedelta(days=days_ahead)

    try:
        return date.fromisoformat(raw) # parse standard iso string
    except ValueError:
        raise ValueError(f"unknown date format: '{text}'") # invalid date string


def parse_csv(path: str | Path, today: date) -> list[Task]:
    """read and parse task records from csv into task instances."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"file not found: '{csv_path}'") # ensure file existence

    expected_headers = ["title", "importance", "effort_h", "deadline"]
    tasks: list[Task] = []

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        try:
            raw_header = next(reader) # read first row
        except StopIteration:
            raise EmptyFileError("csv file is empty") # zero bytes file

        cleaned_header = [col.strip().lower() for col in raw_header]
        if cleaned_header != expected_headers:
            raise EmptyFileError("csv file is missing required headers") # header mismatch

        for line_num, row in enumerate(reader, start=2):
            if not row or not any(cell.strip() for cell in row):
                continue # ignore blank lines
            if len(row) != 4:
                raise ValueError(f"line {line_num} has {len(row)} columns, expected 4") # missing column

            title = row[0].strip()
            if not title:
                raise ValueError(f"line {line_num} title cannot be empty") # empty title check

            try:
                importance = int(row[1].strip())
            except ValueError:
                raise ValueError(f"line {line_num} importance must be an integer") # invalid integer

            try:
                effort_h = float(row[2].strip())
            except ValueError:
                raise ValueError(f"line {line_num} effort_h must be a float") # invalid float

            deadline = parse_due(row[3], today) # parse dynamic deadline string
            tasks.append(Task(title=title, importance=importance, effort_h=effort_h, deadline=deadline))

    if not tasks:
        raise EmptyFileError("csv file contains header only with no records") # header only file

    return tasks