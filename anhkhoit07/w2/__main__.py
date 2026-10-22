import os
from datetime import date
from .models import Task
from .io_utils import load_tasks


def main():
    csv_path = os.path.join(os.path.dirname(__file__), "tasks.csv") # locate csv file in same directory
    if not os.path.exists(csv_path):
        sample_rows = (
            "title,importance,effort_h,deadline\n"
            "DS exam,5,6.0,2026-10-30\n"
            "Assignment,4,1.5,2026-10-27\n"
        )
        with open(csv_path, mode="w", encoding="utf-8") as file:
            file.write(sample_rows) # generate sample csv if absent

    tasks = load_tasks(csv_path) # load tasks from csv
    today = date(2026, 10, 22)
    for task in tasks:
        print(f"Task: {task.title} | Importance: {task.importance} | Effort: {task.effort_h}h | Days left: {task.days_left(today)}") # print task details


if __name__ == "__main__":
    main()