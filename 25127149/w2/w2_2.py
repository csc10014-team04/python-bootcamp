from .w2_1 import Task
import csv
import json

from dataclasses import asdict
from datetime import date
from pathlib import Path

def load_tasks(path) -> list[Task]:
    tasks = []

    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        expected = ["title", "importance", "effort_h", "deadline"]
        if reader.fieldnames != expected:
            raise ValueError("CSV header must be: title,importance,effort_h,deadline")

        for line_number, row in enumerate(reader, start=2):
            try:
                task = Task(
                    title=row["title"].strip(),
                    importance=int(row["importance"]),
                    effort_h=float(row["effort_h"]),
                    deadline=date.fromisoformat(row["deadline"].strip())
                )
                tasks.append(task)

            except (ValueError, TypeError, AttributeError, KeyError) as error:
                raise ValueError(
                    f"Invalid data at line {line_number}: {error}"
                ) from error

    return tasks


def save_json(tasks, path):
    data = []

    for task in tasks:
        item = asdict(task)
        item["deadline"] = task.deadline.isoformat()
        data.append(item)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
