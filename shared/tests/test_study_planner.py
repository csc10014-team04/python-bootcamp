from shared.study_planner import filter_by_hour_threshold

class Task:
    def __init__(self,name,hours):
        self.name=name
        self.hours=hours

def test_filter_by_hour_threshold():
    tasks=[
        Task("Math",1),
        Task("Physics",2),
        Task("Programming",3)
    ]
    result=filter_by_hour_threshold(tasks,2)
    assert [task.name for task in result]==["Math"]