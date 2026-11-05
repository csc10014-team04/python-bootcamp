from dataclasses import dataclass
from datetime import date

@dataclass
class Task:
    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self):
        if not (1 <= self.importance <= 5):
            raise ValueError("importance must be between 1 and 5")
        if self.effort_h < 0:
            raise ValueError("effort_h cannot be negative")

    def days_left(self, today: date) -> int:
        delta = (self.deadline - today).days
        return max(delta, 0)