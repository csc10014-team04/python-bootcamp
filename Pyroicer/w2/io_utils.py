from .models import Task
import csv
import json
from dataclasses import dataclass, asdict
from datetime import datetime, date

def load_tasks(path: str) -> list[Task]:
    tasks = []
    
    with open(path, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        
        required_headers = ["title", "importance", "effort_h", "deadline"]
        if reader.fieldnames != required_headers:
            raise ValueError("CSV header must be: title,importance,effort_h,deadline")

        for row in reader:
            line_num = reader.line_num
            
            if not all(row.get(h) for h in required_headers):
                raise ValueError(f"Line {line_num}: Missing or empty column data.")
            
            try:
                title = str(row["title"]).strip()
                importance = int(row["importance"])
                effort_h = float(row["effort_h"])
                

                deadline_date = datetime.strptime(row['deadline'].strip(), "%Y-%m-%d").date()
                
                if not title:
                    raise ValueError("Title can't be blank.")
                    
            except ValueError as e:
                raise ValueError(f"Line {line_num}: Invalid data format. Detailed error: {e}")

            tasks.append(Task(
                title=title,
                importance=importance,
                effort_h=effort_h,
                deadline=deadline_date
            ))
            
    return tasks

def save_json(tasks: list[Task], path: str) -> None:
    
    def json_serial(obj):
        if isinstance(obj, date):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    serialized_tasks = [asdict(task) for task in tasks]
    
    with open(path, mode='w', encoding="utf-8") as f:
        json.dump(serialized_tasks, f, indent=4, ensure_ascii=False, default=json_serial)
