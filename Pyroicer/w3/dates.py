from datetime import date, timedelta
import re

WEEKDAYS = {
    "mon": 0, "monday": 0,
    "tue": 1, "tuesday": 1,
    "wed": 2, "wednesday": 2,
    "thu": 3, "thursday": 3,
    "fri": 4, "friday": 4,
    "sat": 5, "saturday": 5,
    "sun": 6, "sunday": 6,
}


def parse_due(text: str, today: date) -> date:
    cleaned = text.strip().lower()

    if not cleaned:
        raise ValueError("Empty text")

    if cleaned == "tomorrow":
        return today + timedelta(days=1)

    #in n days
    in_days_match = re.fullmatch(r"in\s+(\d+)\s+days?", cleaned)
    if in_days_match:
        return today + timedelta(days=int(in_days_match.group(1)))

    #weekdays
    if cleaned in WEEKDAYS:
        target_weekday = WEEKDAYS[cleaned]
        days_ahead = (target_weekday - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)

    
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", cleaned):
        try:
            return date.fromisoformat(cleaned) # date format: "YYYY-MM-DD"
        except ValueError as exc:
            raise ValueError(f"Invalid calendar date: {text!r}") from exc

    raise ValueError(f"Unable to parse due date: {text!r}")