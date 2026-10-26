"""Week 2 main script."""

import sys

from .io_utils import load_tasks


def main() -> None:
    """Load and print tasks from command line argument."""
    if len(sys.argv) != 2:
        print("Usage: python -m members.w2 <csv_file>")
        sys.exit(1)

    tasks = load_tasks(sys.argv[1])
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()
