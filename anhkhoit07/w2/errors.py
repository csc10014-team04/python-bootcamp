from models import Task


class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float):
        super().__init__()
        self.needed_h = needed_h
        self.available_h = available_h

    def __str__(self) -> str:
        return f"plan requires {self.needed_h}h but only {self.available_h}h available" # readable error message


def check_feasible(tasks: list[Task], available_h: float) -> None:
    needed_h = sum(task.effort_h for task in tasks) # aggregate total effort
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h) # raise custom exception