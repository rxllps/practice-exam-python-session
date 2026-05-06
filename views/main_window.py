import tkinter as tk
from tkinter import ttk
from views.task_view import TaskView
from views.project_view import ProjectView
from views.user_view import UserView


class MainWindow(tk.Tk):
    def __init__(self, task_controller, project_controller, user_controller) -> None:
        super().__init__()
        self.title("Task Management System")
        self.geometry("1100x700")

        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.task_view = TaskView(notebook, task_controller, project_controller, user_controller)
        self.project_view = ProjectView(notebook, project_controller)
        self.user_view = UserView(notebook, user_controller)

        notebook.add(self.task_view, text="Tasks")
        notebook.add(self.project_view, text="Projects")
        notebook.add(self.user_view, text="Users")
