"""Command-line tool for planning tonight's study tasks."""

import argparse
import sys
from datetime import date
from pathlib import Path

# Add paths to enable importing W2 modules
_CURRENT_DIR = Path(__file__).resolve().parent
_MEMBER_DIR = _CURRENT_DIR.parent
_W2_DIR = _MEMBER_DIR / "W2"
for _p in [str(_MEMBER_DIR), str(_W2_DIR)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from W2.io_utils import load_tasks
    from W2.models import Task
except ImportError:
    from io_utils import load_tasks  # type: ignore[no-redef]
    from models import Task  # type: ignore[no-redef]


def select_tasks(tasks: list[Task], hours: float, today: date) -> list[Task]:
    """Select tasks that fit within available hours, prioritizing earlier deadlines.

    Args:
        tasks: Available study tasks.
        hours: Total available hours.
        today: Reference anchor date.

    Returns:
        List of selected tasks.
    """
    selected: list[Task] = []
    remaining = hours

    for task in sorted(tasks, key=lambda t: (t.deadline, t.title)):
        if task.deadline < today:
            continue
        if task.effort_h <= remaining:
            selected.append(task)
            remaining -= task.effort_h

    return selected


def format_schedule(selected: list[Task], hours: float) -> str:
    """Format selected tasks into a printable schedule string.

    Args:
        selected: Tasks chosen for tonight.
        hours: Available study hours.

    Returns:
        Formatted multi-line schedule string.
    """
    lines = [f"Tonight ({hours:.1f} h):"]
    if not selected:
        lines.append("No tasks fit the available time.")
        return "\n".join(lines)

    max_len = max((len(t.title) for t in selected), default=10)
    target_width = max(max_len + 6, 16)

    for index, task in enumerate(selected, start=1):
        dots_count = max(1, target_width - len(task.title))
        dots = "." * dots_count
        lines.append(f"{index:>2}. {task.title} {dots} {task.effort_h:.1f} h")

    return "\n".join(lines)


def main() -> int:
    """Run the command-line task scheduler.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(description="Study task scheduler CLI")
    parser.add_argument("file", help="Path to tasks CSV file")
    parser.add_argument(
        "--hours", type=float, required=True, help="Available study hours"
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Anchor date in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.is_file():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 1

    if args.hours < 0:
        print("Error: --hours must be non-negative", file=sys.stderr)
        return 1

    try:
        tasks = load_tasks(str(file_path))
    except (ValueError, OSError) as exc:
        print(f"Error loading tasks: {exc}", file=sys.stderr)
        return 1

    selected = select_tasks(tasks, args.hours, args.today)
    print(format_schedule(selected, args.hours))
    return 0


if __name__ == "__main__":
    sys.exit(main())
