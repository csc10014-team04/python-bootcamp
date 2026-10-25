
import csv
import json
from dataclasses import asdict
from datetime import date

from models import Task


def load_tasks(path)->list[Task]:
    tasks=[]
    with open(path,"r",newline="",encoding="utf-8") as file:
        reader=csv.DictReader(file)
        expected=["title","importance","effort_h","deadline"]
        if reader.fieldnames!=expected:
            raise ValueError("Invalid CSV header")
        for line,row in enumerate(reader,start=2):
            try:
                title=row["title"].strip()
                importance=int(row["importance"])
                effort_h=float(row["effort_h"])
                deadline=date.fromisoformat(row["deadline"])
                if not title:
                    raise ValueError("Title cannot be empty")
                tasks.append(Task(title,importance,effort_h,deadline))
            except (ValueError,TypeError,AttributeError) as error:
                raise ValueError(f"Invalid row at line {line}: {error}") from error
    return tasks

def save_json(tasks,path)->None:
    with open(path,"w",encoding="utf-8") as file:
        json.dump([asdict(task) for task in tasks],file,indent=4,default=str)
