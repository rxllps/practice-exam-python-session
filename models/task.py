from datetime import datetime

VALID_STATUSES = {"pending", "in_progress", "completed"}
VALID_PRIORITIES = {1, 2, 3}


class Task:
    def __init__(self, title, description, priority, due_date, project_id, assignee_id) -> None:
        if not title or not title.strip():
            raise ValueError("Task title must not be empty")

        if priority not in VALID_PRIORITIES:
            raise ValueError("Priority must be 1, 2, or 3")

        if not isinstance(due_date, datetime):
            raise TypeError("due_date must be a datetime object")

        if project_id is None or assignee_id is None:
            raise ValueError("project_id and assignee_id must be provided")

        self.id = None
        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.priority = priority
        self.status = "pending"
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status) -> bool:
        if new_status not in VALID_STATUSES:
            raise ValueError("Invalid status for task")

        if self.status == new_status:
            return False

        self.status = new_status
        return True

    def is_overdue(self) -> bool:
        return self.status != "completed" and datetime.now() > self.due_date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date.isoformat(),
            "project_id": self.project_id,
            "assignee_id": self.assignee_id,
        }
