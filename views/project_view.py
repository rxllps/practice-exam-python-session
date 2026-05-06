import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class ProjectView(ttk.Frame):
    def __init__(self, parent, project_controller) -> None:
        super().__init__(parent)
        self.project_controller = project_controller
        self.create_widgets()
        self.refresh_projects()

    def create_widgets(self) -> None:
        form_frame = ttk.LabelFrame(self, text="Add project")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Name").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=60)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Description").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.description_entry = ttk.Entry(form_frame, width=60)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Start date (YYYY-MM-DD HH:MM)").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.start_date_entry = ttk.Entry(form_frame, width=30)
        self.start_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame, text="End date (YYYY-MM-DD HH:MM)").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.end_date_entry = ttk.Entry(form_frame, width=30)
        self.end_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(form_frame, text="Add Project", command=self.add_project).grid(row=4, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "name", "status", "start_date", "end_date"), show="headings", selectmode="browse")
        for col, width in [("id", 40), ("name", 240), ("status", 100), ("start_date", 150), ("end_date", 150)]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_projects).pack(side="left")
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=5)

    def refresh_projects(self) -> None:
        self.tree.delete(*self.tree.get_children())
        projects = self.project_controller.get_all_projects()
        for project in projects:
            self.tree.insert("", "end", values=(project.id, project.name, project.status, project.start_date.strftime('%Y-%m-%d %H:%M'), project.end_date.strftime('%Y-%m-%d %H:%M')))

    def add_project(self) -> None:
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        start_date_text = self.start_date_entry.get().strip()
        end_date_text = self.end_date_entry.get().strip()

        if not name or not start_date_text or not end_date_text:
            messagebox.showwarning("Validation error", "Name, start date and end date are required")
            return

        try:
            start_date = datetime.strptime(start_date_text, "%Y-%m-%d %H:%M")
            end_date = datetime.strptime(end_date_text, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Validation error", "Dates must be in YYYY-MM-DD HH:MM format")
            return

        try:
            self.project_controller.add_project(name, description, start_date, end_date)
            messagebox.showinfo("Success", "Project added successfully")
            self.refresh_projects()
        except Exception as exc:
            messagebox.showerror("Error adding project", str(exc))

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection error", "Select a project first")
            return

        project_id = self.tree.item(selected[0], "values")[0]
        if self.project_controller.delete_project(int(project_id)):
            messagebox.showinfo("Success", "Project deleted")
            self.refresh_projects()
        else:
            messagebox.showerror("Error", "Unable to delete project")
