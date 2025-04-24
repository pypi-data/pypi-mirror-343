from .task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, start_time, end_time):
        task = Task(title, description, start_time, end_time)
        self.tasks.append(task)
        return task

    def list_tasks(self):
        return self.tasks