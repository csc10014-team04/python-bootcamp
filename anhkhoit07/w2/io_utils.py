import csv
import json
from datetime import date
from models import Task


def load_tasks(path: str) -> list[Task]:
    tasks = []
    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        try:
            header = next(reader) # read header row
        except StopIteration:
            return tasks

        for line_num, row in enumerate(reader, start=2): # line 1 is header
            if len(row) != 4:
                raise ValueError(f"invalid row at line {line_num}") # wrong column count
            title, importance_raw, effort_raw, deadline_raw = row
            try:
                importance = int(importance_raw)
                effort_h = float(effort_raw)
                deadline = date.fromisoformat(deadline_raw.strip())
                task = Task(title=title.strip(), importance=importance, effort_h=effort_h, deadline=deadline)
                tasks.append(task)
            except Exception:
                raise ValueError(f"invalid row at line {line_num}") # validation error
    return tasks


def save_json(tasks: list[Task], path: str) -> None:
    data = []
    for task in tasks:
        item = {
            "title": task.title,
            "importance": task.importance,
            "effort_h": task.effort_h,
            "deadline": task.deadline.isoformat() # convert date to string
        }
        data.append(item)
    with open(path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4) # serialize to json