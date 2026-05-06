from datetime import datetime

VALID_STATUSES = {"active", "completed", "on_hold"}


class Project:
    def __init__(self, name, description, start_date, end_date) -> None:
        if not name or not name.strip():
            raise ValueError("Project name must not be empty")

        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise TypeError("start_date and end_date must be datetime objects")

        if end_date < start_date:
            raise ValueError("end_date must be equal to or later than start_date")

        self.id = None
        self.name = name.strip()
        self.description = description.strip() if description else ""
        self.start_date = start_date
        self.end_date = end_date
        self.status = "active"

    def update_status(self, new_status) -> bool:
        if new_status not in VALID_STATUSES:
            raise ValueError("Invalid project status")

        if self.status == new_status:
            return False

        self.status = new_status
        return True

    def get_progress(self) -> float:
        if self.status == "completed":
            return 100.0

        now = datetime.now()
        if now <= self.start_date:
            return 0.0

        duration = (self.end_date - self.start_date).total_seconds()
        if duration <= 0:
            return 100.0 if now >= self.end_date else 0.0

        elapsed = min(now, self.end_date) - self.start_date
        progress = (elapsed.total_seconds() / duration) * 100
        return round(max(0.0, min(100.0, progress)), 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "status": self.status,
        }
