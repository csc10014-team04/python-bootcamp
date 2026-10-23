from dataclasses import dataclass
from datetime import date

@dataclass
class Task:
    title: str
    deadline: date

    def days_left(self,today:date)->int:
        return max(0,(self.deadline-today).days)