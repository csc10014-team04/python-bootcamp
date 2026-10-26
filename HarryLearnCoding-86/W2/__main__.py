"""CLI entry point for the W2 study planner package."""

import sys

from .io_utils import load_tasks


def main() -> None:
    """Print tasks loaded from the specified CSV file."""
    if len(sys.argv) != 2:
        print("Usage: python -m HarryLearnCoding-86.W2 <csv_file>")
        sys.exit(1)

    tasks = load_tasks(sys.argv[1])
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()
