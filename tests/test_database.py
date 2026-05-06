import os
import tempfile
from datetime import datetime, timedelta
from database.database_manager import DatabaseManager
from models.project import Project
from models.user import User
from models.task import Task


class TestDatabaseManager:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()

    def teardown_method(self):
        self.db_manager.close()
        os.unlink(self.temp_db.name)

    def test_create_and_fetch_project(self):
        project = Project("Test", "Desc", datetime.now(), datetime.now() + timedelta(days=5))
        project_id = self.db_manager.add_project(project)
        fetched = self.db_manager.get_project_by_id(project_id)
        assert fetched is not None
        assert fetched.name == "Test"

    def test_create_and_fetch_user(self):
        user = User("tester", "tester@example.com", "developer")
        user_id = self.db_manager.add_user(user)
        fetched = self.db_manager.get_user_by_id(user_id)
        assert fetched is not None
        assert fetched.username == "tester"

    def test_create_and_fetch_task(self):
        project_id = self.db_manager.add_project(Project("Test", "Desc", datetime.now(), datetime.now() + timedelta(days=5)))
        user_id = self.db_manager.add_user(User("tester", "tester@example.com", "developer"))
        task = Task("Task", "Desc", 1, datetime.now() + timedelta(days=1), project_id, user_id)
        task_id = self.db_manager.add_task(task)
        fetched = self.db_manager.get_task_by_id(task_id)
        assert fetched is not None
        assert fetched.title == "Task"

    def test_update_and_delete_task(self):
        project_id = self.db_manager.add_project(Project("Test", "Desc", datetime.now(), datetime.now() + timedelta(days=5)))
        user_id = self.db_manager.add_user(User("tester", "tester@example.com", "developer"))
        task_id = self.db_manager.add_task(Task("Task", "Desc", 1, datetime.now() + timedelta(days=1), project_id, user_id))
        assert self.db_manager.update_task(task_id, title="Updated") is True
        fetched = self.db_manager.get_task_by_id(task_id)
        assert fetched.title == "Updated"
        assert self.db_manager.delete_task(task_id) is True
        assert self.db_manager.get_task_by_id(task_id) is None

    def test_update_and_delete_user(self):
        user_id = self.db_manager.add_user(User("tester", "tester@example.com", "developer"))
        assert self.db_manager.update_user(user_id, email="new@example.com") is True
        assert self.db_manager.get_user_by_id(user_id).email == "new@example.com"
        assert self.db_manager.delete_user(user_id) is True
        assert self.db_manager.get_user_by_id(user_id) is None
