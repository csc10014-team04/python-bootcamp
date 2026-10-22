from pathlib import Path
import sys
from .io_utils import load_tasks

def main() -> None:
    # Look for sample.csv provided via CLI argument, or default to sample.csv in this package directory
    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])
    else:
        csv_path = Path(__file__).parent / "sample.csv"

    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading tasks from: {csv_path}\n")
    tasks = load_tasks(str(csv_path))

    for idx, task in enumerate(tasks, start=1):
        print(
            f"{idx}. {task.title} | Importance: {task.importance} | "
            f"Effort: {task.effort_h}h | Deadline: {task.deadline}"
        )

if __name__ == "__main__":
    main()