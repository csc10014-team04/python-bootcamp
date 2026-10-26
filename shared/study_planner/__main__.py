"""Command-line interface for the integrated study planner."""

import argparse
import sys
from datetime import date

from .allocate import allocate
from .errors import EmptyFileError, InfeasiblePlan, StudyPlannerError
from .io import parse_csv
from .prioritise import prioritise
from .render import render


def run_pipeline(
    csv_path: str,
    hours: float,
    today: date,
    strategy: str = "deadline",
) -> str:
    """Execute the study planner pipeline: parse_csv -> prioritise -> allocate -> render.

    Args:
        csv_path: Path to the tasks CSV file.
        hours: Total available hours tonight.
        today: Reference anchor date.
        strategy: Sort strategy, either "deadline" or "importance".

    Returns:
        Rendered schedule string ready for display.

    Raises:
        FileNotFoundError: If the task file is not found.
        EmptyFileError: If the task file has no tasks.
        InfeasiblePlan: If the tasks cannot be scheduled.
        ValueError: If input arguments or row contents are invalid.
    """
    tasks = parse_csv(csv_path, today=today)
    ordered_tasks = prioritise(tasks, today=today, strategy=strategy)
    selected_tasks = allocate(ordered_tasks, hours=hours)
    return render(selected_tasks, hours=hours)


def main() -> int:
    """CLI entry point for the study planner application.

    Returns:
        0 on success, 1 on error.
    """
    parser = argparse.ArgumentParser(
        prog="shared.study_planner",
        description="Integrated study task planner CLI.",
    )
    parser.add_argument(
        "file",
        help="Path to the tasks CSV file.",
    )
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Available study hours tonight.",
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Anchor date in YYYY-MM-DD format (default: today).",
    )
    parser.add_argument(
        "--strategy",
        choices=["deadline", "importance"],
        default="deadline",
        help="Prioritisation strategy (default: deadline).",
    )
    args = parser.parse_args()

    if args.hours < 0:
        print("Error: --hours must be non-negative", file=sys.stderr)
        return 1

    try:
        output = run_pipeline(
            csv_path=args.file,
            hours=args.hours,
            today=args.today,
            strategy=args.strategy,
        )
        print(output)
        return 0
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 1
    except EmptyFileError as exc:
        print(f"Error: empty file: {exc}", file=sys.stderr)
        return 1
    except InfeasiblePlan as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except (StudyPlannerError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

