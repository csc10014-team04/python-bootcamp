import re
from datetime import date, timedelta


def parse_due(text: str, today: date) -> date:
    raw = text.strip() # remove surrounding whitespace
    lower = raw.lower()

    if lower == "tomorrow":
        return today + timedelta(days=1) # calculate next day date

    match_in_days = re.fullmatch(r"in\s+(\d+)\s+days?", lower)
    if match_in_days:
        offset = int(match_in_days.group(1))
        return today + timedelta(days=offset) # add specified days

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
        days_ahead = (target_idx - today.weekday()) % 7 # calculate day distance
        if days_ahead == 0:
            days_ahead = 7 # move to next occurrence if today
        return today + timedelta(days=days_ahead)

    try:
        return date.fromisoformat(raw) # parse standard iso format
    except ValueError:
        raise ValueError(f"unknown date format: {text}") # raise error for invalid string