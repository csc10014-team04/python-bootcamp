import re
from datetime import date, timedelta

def parse_due(text: str, today: date) -> date:
    text = text.strip().lower()

    if (re.fullmatch(r"\d{4}-\d{2}-\d{2}", text)):
        try:
            return date.fromisoformat(text)
        except ValueError:
            raise ValueError("Invalid date")

    if (text == "tomorrow"):
        return today + timedelta(days=1)

    match = re.fullmatch(r"in (\d+) days?", text)
    if (match):
        return today + timedelta(days=int(match.group(1)))

    weekdays = {
        "mon": 0, "monday": 0,
        "tue": 1, "tues": 1, "tuesday": 1,
        "wed": 2, "wednesday": 2,
        "thu": 3, "thur": 3, "thurs": 3, "thursday": 3,
        "fri": 4, "friday": 4,
        "sat": 5, "saturday": 5,
        "sun": 6, "sunday": 6
    }

    if (text in weekdays):
        days = (weekdays[text] - today.weekday()) % 7
        return today + timedelta(days=days if days > 0 else 7)

    raise ValueError(f"Unknown due date: {text}")