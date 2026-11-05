import csv
import json
from datetime import date
from pathlib import Path
from typing import List
from .models import Task

def load_tasks(path: str | Path) -> List[Task]:
    tasks = []
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            try:
                title = row["title"].strip()
                importance = int(row["importance"])
                effort_h = float(row["effort_h"])
                deadline = date.fromisoformat(row["deadline"].strip())
                tasks.append(Task(title=title, importance=importance, effort_h=effort_h, deadline=deadline))
            except Exception as e:
                raise ValueError(f"Invalid row at line {line_no}: {e}")
    return tasks

def save_json(tasks: List[Task], path: str | Path) -> None:
    path = Path(path)
    data = [
        {
            "title": t.title,
            "importance": t.importance,
            "effort_h": t.effort_h,
            "deadline": t.deadline.isoformat(),
        }
        for t in tasks
    ]
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)