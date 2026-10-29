#!/usr/bin/env python3
import argparse
import csv
from datetime import date, timedelta
from pathlib import Path
import re
import sys

WEEKDAYS = {
    "mon": 0, "monday": 0,
    "tue": 1, "tues": 1, "tuesday": 1,
    "wed": 2, "wednesday": 2,
    "thu": 3, "thur": 3, "thurs": 3, "thursday": 3,
    "fri": 4, "friday": 4,
    "sat": 5, "saturday": 5,
    "sun": 6, "sunday": 6,
}


def parse_due(text: str, today: date) -> date:
    cleaned = text.strip().lower()
    if not cleaned:
        raise ValueError("Due date text cannot be empty.")

    if cleaned == "tomorrow":
        return today + timedelta(days=1)

    in_days_match = re.fullmatch(r"in\s+(\d+)\s+days?", cleaned)
    if in_days_match:
        return today + timedelta(days=int(in_days_match.group(1)))

    if cleaned in WEEKDAYS:
        target_weekday = WEEKDAYS[cleaned]
        days_ahead = (target_weekday - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", cleaned):
        try:
            return date.fromisoformat(cleaned)
        except ValueError as exc:
            raise ValueError(f"Invalid calendar date: {text!r}") from exc

    raise ValueError(f"Unable to parse due date: {text!r}")


def parse_date_arg(val: str) -> date:
    try:
        return date.fromisoformat(val)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{val}'. Expected YYYY-MM-DD.")


def load_tasks(csv_path: Path, today: date) -> list[dict]:
    tasks = []
    with csv_path.open(mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("title") or row.get("task") or row.get("name")
            due_raw = row.get("due") or row.get("due_date")
            hours_raw = row.get("hours") or row.get("duration")

            if not (title and due_raw and hours_raw):
                continue

            tasks.append({
                "title": title.strip(),
                "due": parse_due(due_raw, today),
                "hours": float(hours_raw),
            })
    return tasks


def schedule_tasks(tasks: list[dict], available_hours: float) -> list[dict]:
    # Sort by urgency (earliest due date first), then by shorter duration
    sorted_tasks = sorted(tasks, key=lambda t: (t["due"], t["hours"]))
    
    selected = []
    remaining = available_hours

    for task in sorted_tasks:
        if remaining <= 0:
            break
        allocated = min(task["hours"], remaining)
        if allocated > 0:
            selected.append({"title": task["title"], "hours": allocated})
            remaining -= allocated

    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI scheduler for daily tasks.")
    parser.add_argument("file", type=Path, help="Path to the tasks CSV file.")
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Available study/work hours for tonight.",
    )
    parser.add_argument(
        "--today",
        type=parse_date_arg,
        default=date.today(),
        help="Reference date in YYYY-MM-DD format (default: today).",
    )

    args = parser.parse_args()

    if not args.file.is_file():
        sys.stderr.write(f"Error: File not found: '{args.file}'\n")
        sys.exit(1)

    try:
        tasks = load_tasks(args.file, args.today)
    except Exception as exc:
        sys.stderr.write(f"Error parsing tasks file: {exc}\n")
        sys.exit(1)

    scheduled = schedule_tasks(tasks, args.hours)

    print(f"Tonight ({args.hours:.1f} h):")
    total_width = 24
    for i, item in enumerate(scheduled, 1):
        prefix = f"{i}. {item['title']} "
        suffix = f" {item['hours']:.1f} h"
        dots_count = max(1, total_width - len(prefix) - len(suffix))
        dots = "." * dots_count
        print(f"{prefix}{dots}{suffix}")


if __name__ == "__main__":
    main()