from pathlib import Path
from .io_utils import load_tasks

def main():
    sample_path = Path("samples/tasks.csv")
    if not sample_path.exists():
        print(f"Sample file not found at {sample_path}")
        return
    tasks = load_tasks(sample_path)
    print(f"Loaded {len(tasks)} tasks from {sample_path}:")
    for t in tasks:
        print(f"- {t.title} (Importance: {t.importance}, Effort: {t.effort_h}h, Deadline: {t.deadline})")

if __name__ == "__main__":
    main()