import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class TaskView(ttk.Frame):
    def __init__(self, parent, task_controller, project_controller, user_controller) -> None:
        super().__init__(parent)
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self) -> None:
        form_frame = ttk.LabelFrame(self, text="Add task")
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = ["Title", "Description", "Priority", "Due date (YYYY-MM-DD HH:MM)", "Project ID", "Assignee ID"]
        for idx, text in enumerate(labels):
            ttk.Label(form_frame, text=text).grid(row=idx, column=0, sticky="w", padx=5, pady=5)

        self.title_entry = ttk.Entry(form_frame, width=60)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.description_entry = ttk.Entry(form_frame, width=60)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        self.priority_var = tk.StringVar(value="1")
        self.priority_combo = ttk.Combobox(
            form_frame,
            textvariable=self.priority_var,
            values=["1", "2", "3"],
            width=10,
            state="readonly",
        )
        self.priority_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.due_date_entry = ttk.Entry(form_frame, width=30)
        self.due_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.project_id_entry = ttk.Entry(form_frame, width=20)
        self.project_id_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.assignee_id_entry = ttk.Entry(form_frame, width=20)
        self.assignee_id_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(form_frame, text="Add Task", command=self.add_task).grid(row=6, column=0, columnspan=2, pady=10)

        filter_frame = ttk.LabelFrame(self, text="Search and filter")
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Search").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(filter_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(filter_frame, text="Find", command=self.refresh_tasks).grid(row=0, column=2, padx=5)

        ttk.Label(filter_frame, text="Status").grid(row=1, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar(value="All")
        self.status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=["All", "pending", "in_progress", "completed"],
            state="readonly",
            width=15,
        )
        self.status_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.status_combo.bind("<<ComboboxSelected>>", lambda _: self.refresh_tasks())

        ttk.Label(filter_frame, text="Priority").grid(row=1, column=2, padx=5, pady=5)
        self.priority_filter = tk.StringVar(value="All")
        self.priority_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.priority_filter,
            values=["All", "1", "2", "3"],
            state="readonly",
            width=10,
        )
        self.priority_combo.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.priority_combo.bind("<<ComboboxSelected>>", lambda _: self.refresh_tasks())

        self.tree = ttk.Treeview(
            self,
            columns=(
                "id",
                "title",
                "priority",
                "status",
                "due_date",
                "project_id",
                "assignee_id",
            ),
            show="headings",
            selectmode="browse",
        )
        for col, width in [
            ("id", 40),
            ("title", 220),
            ("priority", 80),
            ("status", 100),
            ("due_date", 150),
            ("project_id", 80),
            ("assignee_id", 80),
        ]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_tasks).pack(side="left")
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=5)

    def refresh_tasks(self) -> None:
        self.tree.delete(*self.tree.get_children())
        tasks = self.task_controller.get_all_tasks()
        query = self.search_entry.get().strip().lower()
        if query:
            tasks = [
                task
                for task in tasks
                if query in task.title.lower() or query in task.description.lower()
            ]

        status = self.status_var.get()
        if status and status != "All":
            tasks = [task for task in tasks if task.status == status]

        priority = self.priority_filter.get()
        if priority and priority != "All":
            tasks = [task for task in tasks if str(task.priority) == priority]

        for task in tasks:
            self.tree.insert(
                "",
                "end",
                values=(
                    task.id,
                    task.title,
                    task.priority,
                    task.status,
                    task.due_date.strftime("%Y-%m-%d %H:%M"),
                    task.project_id,
                    task.assignee_id,
                ),
            )

    def add_task(self) -> None:
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        priority = int(self.priority_var.get())
        due_date_text = self.due_date_entry.get().strip()
        project_id = self.project_id_entry.get().strip()
        assignee_id = self.assignee_id_entry.get().strip()

        if not title or not due_date_text or not project_id or not assignee_id:
            messagebox.showwarning(
                "Validation error",
                "Title, due date, project ID and assignee ID are required",
            )
            return

        try:
            due_date = datetime.strptime(due_date_text, "%Y-%m-%d %H:%M")
            project_id = int(project_id)
            assignee_id = int(assignee_id)
        except ValueError:
            messagebox.showerror(
                "Validation error",
                "Please provide correct types for due date, project ID and assignee ID",
            )
            return

        try:
            self.task_controller.add_task(title, description, priority, due_date, project_id, assignee_id)
            messagebox.showinfo("Success", "Task added successfully")
            self.refresh_tasks()
        except Exception as exc:
            messagebox.showerror("Error adding task", str(exc))

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection error", "Select a task first")
            return

        task_id = self.tree.item(selected[0], "values")[0]
        if self.task_controller.delete_task(int(task_id)):
            messagebox.showinfo("Success", "Task deleted")
            self.refresh_tasks()
        else:
            messagebox.showerror("Error", "Unable to delete task")
