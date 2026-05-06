import sqlite3
from datetime import datetime
from models.task import Task
from models.project import Project
from models.user import User


class DatabaseManager:
    def __init__(self, db_path="tasks.db") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_tables(self) -> None:
        self.create_project_table()
        self.create_user_table()
        self.create_task_table()
        self.conn.commit()

    def create_task_table(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER NOT NULL,
                status TEXT NOT NULL,
                due_date TEXT NOT NULL,
                project_id INTEGER NOT NULL,
                assignee_id INTEGER NOT NULL,
                FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
                FOREIGN KEY(assignee_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )

    def create_project_table(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )

    def create_user_table(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                registration_date TEXT NOT NULL
            )
            """
        )

    def add_task(self, task: Task) -> int:
        if not isinstance(task, Task):
            raise TypeError("Expected Task instance")

        cursor = self.conn.execute(
            "INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                task.title,
                task.description,
                task.priority,
                task.status,
                task.due_date.isoformat(),
                task.project_id,
                task.assignee_id,
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_task_by_id(self, task_id) -> Task | None:
        row = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return self._row_to_task(row)

    def get_all_tasks(self) -> list[Task]:
        rows = self.conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        return [self._row_to_task(row) for row in rows]

    def update_task(self, task_id, **kwargs) -> bool:
        allowed = {"title", "description", "priority", "status", "due_date", "project_id", "assignee_id"}
        if not kwargs:
            return False

        fields = []
        values = []
        for key, value in kwargs.items():
            if key not in allowed:
                raise ValueError(f"Invalid field for task update: {key}")
            if key == "due_date" and isinstance(value, datetime):
                value = value.isoformat()
            fields.append(f"{key} = ?")
            values.append(value)

        values.append(task_id)
        query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
        cursor = self.conn.execute(query, tuple(values))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_task(self, task_id) -> bool:
        cursor = self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def search_tasks(self, query) -> list[Task]:
        pattern = f"%{query}%"
        rows = self.conn.execute(
            "SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ? ORDER BY id",
            (pattern, pattern),
        ).fetchall()
        return [self._row_to_task(row) for row in rows]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        rows = self.conn.execute("SELECT * FROM tasks WHERE project_id = ? ORDER BY id", (project_id,)).fetchall()
        return [self._row_to_task(row) for row in rows]

    def get_tasks_by_user(self, user_id) -> list[Task]:
        rows = self.conn.execute("SELECT * FROM tasks WHERE assignee_id = ? ORDER BY id", (user_id,)).fetchall()
        return [self._row_to_task(row) for row in rows]

    def add_project(self, project: Project) -> int:
        if not isinstance(project, Project):
            raise TypeError("Expected Project instance")

        cursor = self.conn.execute(
            "INSERT INTO projects (name, description, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)",
            (
                project.name,
                project.description,
                project.start_date.isoformat(),
                project.end_date.isoformat(),
                project.status,
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_project_by_id(self, project_id) -> Project | None:
        row = self.conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        return self._row_to_project(row)

    def get_all_projects(self) -> list[Project]:
        rows = self.conn.execute("SELECT * FROM projects ORDER BY id").fetchall()
        return [self._row_to_project(row) for row in rows]

    def update_project(self, project_id, **kwargs) -> bool:
        allowed = {"name", "description", "start_date", "end_date", "status"}
        if not kwargs:
            return False

        fields = []
        values = []
        for key, value in kwargs.items():
            if key not in allowed:
                raise ValueError(f"Invalid field for project update: {key}")
            if key in {"start_date", "end_date"} and isinstance(value, datetime):
                value = value.isoformat()
            fields.append(f"{key} = ?")
            values.append(value)

        values.append(project_id)
        query = f"UPDATE projects SET {', '.join(fields)} WHERE id = ?"
        cursor = self.conn.execute(query, tuple(values))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_project(self, project_id) -> bool:
        cursor = self.conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def add_user(self, user: User) -> int:
        if not isinstance(user, User):
            raise TypeError("Expected User instance")

        cursor = self.conn.execute(
            "INSERT INTO users (username, email, role, registration_date) VALUES (?, ?, ?, ?)",
            (
                user.username,
                user.email,
                user.role,
                user.registration_date.isoformat(),
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_id(self, user_id) -> User | None:
        row = self.conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return self._row_to_user(row)

    def get_all_users(self) -> list[User]:
        rows = self.conn.execute("SELECT * FROM users ORDER BY id").fetchall()
        return [self._row_to_user(row) for row in rows]

    def update_user(self, user_id, **kwargs) -> bool:
        allowed = {"username", "email", "role"}
        if not kwargs:
            return False

        fields = []
        values = []
        for key, value in kwargs.items():
            if key not in allowed:
                raise ValueError(f"Invalid field for user update: {key}")
            fields.append(f"{key} = ?")
            values.append(value)

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        cursor = self.conn.execute(query, tuple(values))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_user(self, user_id) -> bool:
        cursor = self.conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def _row_to_task(self, row):
        if row is None:
            return None

        task = Task(
            row["title"],
            row["description"],
            row["priority"],
            self._to_datetime(row["due_date"]),
            row["project_id"],
            row["assignee_id"],
        )
        task.id = row["id"]
        task.status = row["status"]
        return task

    def _row_to_project(self, row):
        if row is None:
            return None

        project = Project(
            row["name"],
            row["description"],
            self._to_datetime(row["start_date"]),
            self._to_datetime(row["end_date"]),
        )
        project.id = row["id"]
        project.status = row["status"]
        return project

    def _row_to_user(self, row):
        if row is None:
            return None

        user = User(row["username"], row["email"], row["role"])
        user.id = row["id"]
        user.registration_date = self._to_datetime(row["registration_date"])
        return user

    def _to_datetime(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value)
