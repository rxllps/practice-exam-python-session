from datetime import datetime
import re

VALID_ROLES = {"admin", "manager", "developer"}
EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$")


class User:
    def __init__(self, username, email, role) -> None:
        if not username or not username.strip():
            raise ValueError("Username must not be empty")

        if not self._is_valid_email(email):
            raise ValueError("Invalid email address")

        if role not in VALID_ROLES:
            raise ValueError("Role must be admin, manager, or developer")

        self.id = None
        self.username = username.strip()
        self.email = email.strip()
        self.role = role
        self.registration_date = datetime.now()

    def _is_valid_email(self, email) -> bool:
        if not isinstance(email, str):
            return False
        return bool(EMAIL_PATTERN.match(email.strip()))

    def update_info(self, username=None, email=None, role=None) -> None:
        if username is not None:
            if not username.strip():
                raise ValueError("Username must not be empty")
            self.username = username.strip()

        if email is not None:
            if not self._is_valid_email(email):
                raise ValueError("Invalid email address")
            self.email = email.strip()

        if role is not None:
            if role not in VALID_ROLES:
                raise ValueError("Role must be admin, manager, or developer")
            self.role = role

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "registration_date": self.registration_date.isoformat(),
        }
