"""Plan tasks that fit within an available number of hours."""

import argparse
import sys
from datetime import date
from pathlib import Path

from w2.w2_1 import Task
from w2.w2_2 import load_tasks


def plan_tasks(
    tasks: list[Task],
    available_h: float,
    today: date,
) -> list[Task]:
    """Select tasks that fit, prioritizing earliest deadline then importance."""
    if available_h < 0:
        raise ValueError("Available hours cannot be negative")

    sorted_tasks = sorted(
        tasks,
        key=lambda task: (task.days_left(today), -task.importance),
    )
    planned: list[Task] = []
    remaining_h = available_h
    for task in sorted_tasks:
        if task.effort_h <= remaining_h:
            planned.append(task)
            remaining_h -= task.effort_h
    return planned


def main() -> int:
    """Parse command-line arguments, plan tasks, and print the result."""
    parser = argparse.ArgumentParser(
        description="Plan tasks based on available hours and today's date."
    )
    parser.add_argument("file", help="Path to the tasks CSV file")
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Available hours for tonight",
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Reference date in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args()

    if not Path(args.file).is_file():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 1

    try:
        tasks = load_tasks(args.file)
        planned = plan_tasks(tasks, available_h=args.hours, today=args.today)
        print(f"Tonight ({args.hours:.1f} h):")
        for index, task in enumerate(planned, start=1):
            print(f" {index}. {task.title} ...... {task.effort_h:.1f} h")
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
