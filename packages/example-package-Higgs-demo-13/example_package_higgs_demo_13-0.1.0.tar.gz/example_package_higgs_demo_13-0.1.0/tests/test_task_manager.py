import pytest
from calendar_app_package.manager import TaskManager
from calendar_app_package.task import Task

def test_add_and_list_tasks():
    manager = TaskManager()
    task = manager.add_task(
        "Test Task",
        "Testing manager add",
        "2025-05-01T10:00:00",
        "2025-05-01T11:00:00"
    )
    tasks = manager.list_tasks()

    assert len(tasks) == 1
    assert tasks[0] == task
    assert task.title == "Test Task"
    assert task.description == "Testing manager add"

def test_task_str_format():
    task = Task(
        "Example wa wa wa",
        "wawawa",
        "2025-05-02T09:00:00",
        "2025-05-02T10:00:00"
    )
    expected_str = "Example wa wa wa: 2025-05-02T09:00:00 → 2025-05-02T10:00:00"
    assert str(task) == expected_str