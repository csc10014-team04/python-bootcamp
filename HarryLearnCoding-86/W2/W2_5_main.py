import sys
from .io_utils import load_tasks

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m members.w2 <csv_file>")
        sys.exit(1)
    
    tasks = load_tasks(sys.argv[1])
    for task in tasks:
        print(task)