#!/usr/bin/env python3
import os
import sys
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database.database_manager import DatabaseManager
    from controllers.task_controller import TaskController
    from controllers.project_controller import ProjectController
    from controllers.user_controller import UserController
    from views.main_window import MainWindow
except ImportError as error:
    print(f"Import error: {error}")
    sys.exit(1)


def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(base_dir, "database")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "tasks.db")

        db_manager = DatabaseManager(db_path)
        db_manager.create_tables()

        task_controller = TaskController(db_manager)
        project_controller = ProjectController(db_manager)
        user_controller = UserController(db_manager)

        root = MainWindow(task_controller, project_controller, user_controller)
        root.mainloop()
    except Exception as exc:
        messagebox.showerror("Error", str(exc))
        print(str(exc))
        sys.exit(1)


if __name__ == "__main__":
    main()
