"""Parse natural-language due dates into calendar dates."""

import re
from datetime import date, timedelta


def parse_due(text: str, today: date) -> date:
    """Parse ISO dates, relative day expressions, or weekday names.

    Weekday names refer to the next occurrence; a name matching today means
    seven days from today.
    """
    normalized_text = text.strip().lower()
    try:
        return date.fromisoformat(normalized_text)
    except ValueError:
        pass

    if normalized_text == "tomorrow":
        return today + timedelta(days=1)

    match = re.fullmatch(r"in\s+(\d+)\s+days?", normalized_text)
    if match:
        return today + timedelta(days=int(match.group(1)))

    weekdays = {
        "mon": 0, "monday": 0,
        "tue": 1, "tuesday": 1,
        "wed": 2, "wednesday": 2,
        "thu": 3, "thursday": 3,
        "fri": 4, "friday": 4,
        "sat": 5, "saturday": 5,
        "sun": 6, "sunday": 6,
    }
    if normalized_text in weekdays:
        target_day = weekdays[normalized_text]
        days_ahead = (target_day - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)

    raise ValueError(f"Unknown due date: {text}")
