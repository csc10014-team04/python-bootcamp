from pathlib import Path
from .w2_2 import load_tasks
def main():
    csv_path = Path(__file__).parent / "tasks.csv"

    if not csv_path.exists():
        print(f"Error: Not found file {csv_path}")
        return

    print(f"--- Loading tasks: {csv_path.name} ---")
    tasks = load_tasks(csv_path)

    for idx, task in enumerate(tasks, start=1):
        print(f"{idx}. [{task.importance}/5] {task.title} - Time: {task.effort_h}h - Deadline: {task.deadline}")

if __name__ == "__main__":
    main()
