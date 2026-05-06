import tkinter as tk
from tkinter import ttk, messagebox


class UserView(ttk.Frame):
    def __init__(self, parent, user_controller) -> None:
        super().__init__(parent)
        self.user_controller = user_controller
        self.create_widgets()
        self.refresh_users()

    def create_widgets(self) -> None:
        form_frame = ttk.LabelFrame(self, text="Add user")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Username").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = ttk.Entry(form_frame, width=40)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Role").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.role_var = tk.StringVar(value="developer")
        self.role_combo = ttk.Combobox(
            form_frame,
            textvariable=self.role_var,
            values=["admin", "manager", "developer"],
            state="readonly",
            width=20,
        )
        self.role_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(form_frame, text="Add User", command=self.add_user).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        self.tree = ttk.Treeview(
            self, columns=("id", "username", "email", "role"), show="headings", selectmode="browse"
        )
        for col, width in [
            ("id", 40),
            ("username", 200),
            ("email", 240),
            ("role", 100),
        ]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_users).pack(side="left")
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=5)

    def refresh_users(self) -> None:
        self.tree.delete(*self.tree.get_children())
        users = self.user_controller.get_all_users()
        for user in users:
            self.tree.insert("", "end", values=(user.id, user.username, user.email, user.role))

    def add_user(self) -> None:
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        role = self.role_var.get()

        if not username or not email:
            messagebox.showwarning("Validation error", "Username and email are required")
            return

        try:
            self.user_controller.add_user(username, email, role)
            messagebox.showinfo("Success", "User added successfully")
            self.refresh_users()
        except Exception as exc:
            messagebox.showerror("Error adding user", str(exc))

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection error", "Select a user first")
            return

        user_id = self.tree.item(selected[0], "values")[0]
        if self.user_controller.delete_user(int(user_id)):
            messagebox.showinfo("Success", "User deleted")
            self.refresh_users()
        else:
            messagebox.showerror("Error", "Unable to delete user")
