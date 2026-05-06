from datetime import datetime
from models.task import Task


class TaskController:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def add_task(self, title, description, priority, due_date, project_id, assignee_id) -> int:
        if not isinstance(due_date, datetime):
            raise TypeError("due_date must be a datetime object")

        if self.db_manager.get_project_by_id(project_id) is None:
            raise ValueError("Project does not exist")

        if self.db_manager.get_user_by_id(assignee_id) is None:
            raise ValueError("User does not exist")

        task = Task(title, description, priority, due_date, project_id, assignee_id)
        return self.db_manager.add_task(task)

    def get_task(self, task_id) -> Task | None:
        return self.db_manager.get_task_by_id(task_id)

    def get_all_tasks(self) -> list[Task]:
        return self.db_manager.get_all_tasks()

    def update_task(self, task_id, **kwargs) -> bool:
        if "due_date" in kwargs and isinstance(kwargs["due_date"], str):
            raise TypeError("due_date must be a datetime object")
        return self.db_manager.update_task(task_id, **kwargs)

    def delete_task(self, task_id) -> bool:
        return self.db_manager.delete_task(task_id)

    def search_tasks(self, query) -> list[Task]:
        return self.db_manager.search_tasks(query)

    def update_task_status(self, task_id, new_status) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.update_status(new_status)
        return self.db_manager.update_task(task_id, status=new_status)

    def get_overdue_tasks(self) -> list[Task]:
        return [task for task in self.get_all_tasks() if task.is_overdue()]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        return self.db_manager.get_tasks_by_project(project_id)

    def get_tasks_by_user(self, user_id) -> list[Task]:
        return self.db_manager.get_tasks_by_user(user_id)
