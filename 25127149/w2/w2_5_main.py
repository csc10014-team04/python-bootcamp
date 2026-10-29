"""Load and display tasks from the sample CSV file."""

from pathlib import Path

from w2.w2_2 import load_tasks


def main() -> int:
    """Print the tasks in tasks.csv; return nonzero if the file is missing."""
    csv_path = Path(__file__).parent / "tasks.csv"
    if not csv_path.exists():
        print(f"Error: Not found file {csv_path}")
        return 1

    print(f"--- Loading tasks: {csv_path.name} ---")
    tasks = load_tasks(csv_path)
    for index, task in enumerate(tasks, start=1):
        print(
            f"{index}. [{task.importance}/5] {task.title} - "
            f"Time: {task.effort_h}h - Deadline: {task.deadline}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
