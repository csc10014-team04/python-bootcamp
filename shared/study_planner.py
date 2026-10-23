def filter_by_hour_threshold(tasks,threshold):
    return [task for task in tasks if task.hours<threshold]