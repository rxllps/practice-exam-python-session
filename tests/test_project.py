import sys
import os
from datetime import datetime, timedelta
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from database.database_manager import DatabaseManager
from controllers.project_controller import ProjectController
from controllers.task_controller import TaskController
from models.user import User


class TestProjectController:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()
        self.controller = ProjectController(self.db_manager)

    def teardown_method(self):
        self.db_manager.close()
        os.unlink(self.temp_db.name)

    def test_add_project(self):
        project_id = self.controller.add_project(
            "Новый проект",
            "Описание нового проекта",
            datetime.now(),
            datetime.now() + timedelta(days=30),
        )

        assert project_id is not None
        assert isinstance(project_id, int)

        project = self.controller.get_project(project_id)
        assert project.name == "Новый проект"
        assert project.description == "Описание нового проекта"
        assert project.status == "active"

    def test_get_project(self):
        project_id = self.controller.add_project(
            "Проект для получения",
            "Описание",
            datetime.now(),
            datetime.now() + timedelta(days=30),
        )

        project = self.controller.get_project(project_id)
        assert project is not None
        assert project.name == "Проект для получения"
        assert project.status == "active"

    def test_get_all_projects(self):
        self.controller.add_project("Проект 1", "Описание 1", datetime.now(), datetime.now() + timedelta(days=10))
        self.controller.add_project("Проект 2", "Описание 2", datetime.now(), datetime.now() + timedelta(days=20))

        projects = self.controller.get_all_projects()
        assert len(projects) >= 2
        for project in projects:
            assert hasattr(project, "id")
            assert hasattr(project, "name")
            assert hasattr(project, "status")

    def test_update_project(self):
        project_id = self.controller.add_project(
            "Старое название",
            "Старое описание",
            datetime.now(),
            datetime.now() + timedelta(days=10),
        )

        self.controller.update_project(
            project_id,
            name="Новое название",
            description="Новое описание",
        )

        project = self.controller.get_project(project_id)
        assert project.name == "Новое название"
        assert project.description == "Новое описание"

    def test_delete_project(self):
        project_id = self.controller.add_project(
            "Проект для удаления",
            "Описание",
            datetime.now(),
            datetime.now() + timedelta(days=10),
        )

        self.controller.delete_project(project_id)
        project = self.controller.get_project(project_id)
        assert project is None

    def test_update_project_status(self):
        project_id = self.controller.add_project(
            "Проект для смены статуса",
            "Описание",
            datetime.now(),
            datetime.now() + timedelta(days=10),
        )

        self.controller.update_project_status(project_id, "completed")
        project = self.controller.get_project(project_id)
        assert project.status == "completed"

    def test_get_project_progress(self):
        project_id = self.controller.add_project(
            "Проект для прогресса",
            "Описание",
            datetime.now(),
            datetime.now() + timedelta(days=10),
        )

        task_controller = TaskController(self.db_manager)
        user_id = self.db_manager.add_user(User("test", "test@example.com", "developer"))

        task_controller.add_task("Задача 1", "Описание", 1, datetime.now() + timedelta(days=1), project_id, user_id)
        task_controller.add_task("Задача 2", "Описание", 1, datetime.now() + timedelta(days=1), project_id, user_id)

        tasks = task_controller.get_tasks_by_project(project_id)
        if tasks:
            task_controller.update_task_status(tasks[0].id, "completed")

        progress = self.controller.get_project_progress(project_id)
        assert isinstance(progress, float)
        assert 0 <= progress <= 100
