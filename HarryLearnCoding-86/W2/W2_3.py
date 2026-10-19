from .models import Task

class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float):
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(self.__str__())

    def __str__(self):
        return f"Infeasible Plan: requires {self.needed_h}h, but only {self.available_h}h available."

def check_feasible(tasks: list[Task], available_h: float):
    needed_h = sum(t.effort_h for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)