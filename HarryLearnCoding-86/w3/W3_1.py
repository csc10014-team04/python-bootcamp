"""Date parsing utilities for the study planner."""

import re
from datetime import date, timedelta

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


def parse_due(text: str, today: date) -> date:
    """Parse a human-readable due date description into a date object.

    Accepts:
        - ISO date format: "YYYY-MM-DD" (e.g. "2026-10-30")
        - "tomorrow": one day after today
        - "in N days" or "in N day": N days after today
        - Weekday names (e.g. "Fri", "Friday"): next occurrence (1-7 days away)

    Args:
        text: Due date text to parse.
        today: Reference anchor date.

    Returns:
        The computed due date.

    Raises:
        ValueError: If the text cannot be recognized or represents an invalid date.
    """
    clean = text.strip().lower()
    if not clean:
        raise ValueError("Due date text cannot be empty")

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", clean):
        try:
            return date.fromisoformat(clean)
        except ValueError as exc:
            raise ValueError(f"Invalid date: {text}") from exc

    if clean == "tomorrow":
        return today + timedelta(days=1)

    match = re.fullmatch(r"in\s+(\d+)\s+days?", clean)
    if match:
        return today + timedelta(days=int(match.group(1)))

    if clean in _WEEKDAYS:
        target_weekday = _WEEKDAYS[clean]
        days_ahead = (target_weekday - today.weekday()) % 7
        return today + timedelta(days=days_ahead if days_ahead > 0 else 7)

    raise ValueError(f"Unknown due date: {text}")
