from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self):
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be 1-5") # validate importance range

    def days_left(self, today: date) -> int:
        delta = (self.deadline - today).days # calculate date difference
        return max(0, delta) # ensure non-negative days