from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """task representation containing scheduling metadata."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be between 1 and 5") # validate importance bounds
        if self.effort_h < 0:
            raise ValueError("effort_h must be non-negative") # validate effort bounds

    def days_left(self, today: date) -> int:
        """calculate days remaining until deadline."""
        delta = (self.deadline - today).days # compute date delta
        return max(0, delta) # bound minimum to zero