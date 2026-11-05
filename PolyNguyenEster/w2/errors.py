class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float):
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(f"Infeasible plan: needed {needed_h}h, but only {available_h}h available.")

def check_feasible(tasks: list, available_h: float) -> None:
    total_needed = sum(t.effort_h for t in tasks)
    if total_needed > available_h:
        raise InfeasiblePlan(total_needed, available_h)