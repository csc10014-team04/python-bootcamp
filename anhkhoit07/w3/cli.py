import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class Task:
    title: str
    importance: int
    effort_h: float
    deadline: date

    def days_left(self, today: date) -> int:
        delta = (self.deadline - today).days # compute remaining days
        return max(0, delta)


@dataclass
class Block:
    task: Task
    hours: float


def load_tasks(path: Path) -> list[Task]:
    tasks = []
    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None) # skip csv header row
        for row in reader:
            if not row or len(row) != 4:
                continue
            title, imp_str, eff_str, dl_str = row
            task = Task(
                title=title.strip(),
                importance=int(imp_str.strip()),
                effort_h=float(eff_str.strip()),
                deadline=date.fromisoformat(dl_str.strip())
            )
            tasks.append(task)
    return tasks


def prioritise(tasks: list[Task], today: date) -> list[Task]:
    def priority_score(task: Task) -> float:
        remaining = task.days_left(today)
        if remaining == 0:
            return float("inf") # prioritize overdue tasks
        return task.importance / remaining # compute priority ratio

    return sorted(tasks, key=priority_score, reverse=True) # sort tasks descending


def allocate(tasks: list[Task], total_hours: float) -> list[Block]:
    blocks = []
    budget = total_hours
    for task in tasks:
        if budget <= 0:
            break
        assigned = min(task.effort_h, budget) # allocate up to remaining budget
        if assigned > 0:
            blocks.append(Block(task=task, hours=assigned))
            budget -= assigned
    return blocks


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Study planner command line interface") # init argument parser
    parser.add_argument("csv_path", type=Path, help="path to tasks csv file")
    parser.add_argument("--hours", type=float, required=True, help="total study hours available")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(), help="date anchor formatted as YYYY-MM-DD")
    return parser.parse_args()


def main():
    args = parse_arguments()
    csv_file: Path = args.csv_path

    if not csv_file.is_file():
        sys.stderr.write(f"Error: file '{csv_file}' not found.\n") # write clear error message
        sys.exit(1) # exit with status code 1

    tasks = load_tasks(csv_file)
    prioritised_tasks = prioritise(tasks, args.today)
    allocated_blocks = allocate(prioritised_tasks, args.hours)

    print(f"Tonight ({args.hours:.1f} h):")
    for idx, block in enumerate(allocated_blocks, start=1):
        prefix = f"  {idx}. {block.task.title} "
        line = prefix.ljust(22, ".") + f" {block.hours:.1f} h" # align dot padding
        print(line)


if __name__ == "__main__":
    main()