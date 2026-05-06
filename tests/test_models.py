import pytest
from datetime import datetime, timedelta
from models.task import Task
from models.project import Project
from models.user import User


def test_task_creation_and_status():
    due_date = datetime.now() + timedelta(days=1)
    task = Task("Task", "Description", 2, due_date, 1, 1)
    assert task.title == "Task"
    assert task.status == "pending"
    assert task.is_overdue() is False

    assert task.update_status("in_progress") is True
    assert task.status == "in_progress"
    assert task.update_status("in_progress") is False
    assert task.update_status("completed") is True


def test_project_creation_and_progress():
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=1)
    project = Project("Project", "Desc", start_date, end_date)
    assert project.name == "Project"
    assert project.status == "active"
    progress = project.get_progress()
    assert 0 <= progress <= 100

    assert project.update_status("completed") is True
    assert project.status == "completed"
    assert project.get_progress() == 100.0


def test_user_creation_and_update():
    user = User("username", "user@example.com", "developer")
    assert user.username == "username"
    assert user.role == "developer"
    assert user.email == "user@example.com"

    user.update_info(username="newname", email="new@example.com", role="manager")
    assert user.username == "newname"
    assert user.email == "new@example.com"
    assert user.role == "manager"

    with pytest.raises(ValueError):
        User("", "bad@example.com", "developer")

    with pytest.raises(ValueError):
        User("user", "invalid-email", "developer")

    with pytest.raises(ValueError):
        User("user", "user@example.com", "invalid")
