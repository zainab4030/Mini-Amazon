# users.py
import hashlib
from storage import load_json, save_json

USERS_PATH = "data/users.json"

class UserManager:
    def __init__(self):
        self.users = load_json(USERS_PATH, default=[])

    def _save(self):
        save_json(USERS_PATH, self.users)

    def user_exists(self, username: str) -> bool:
        return any(u["username"] == username for u in self.users)

    def _hash_pw(self, password: str) -> str:
        # Bonus extension: hashing (recommended but optional in handout)
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def register(self, username: str, password: str) -> tuple[bool, str]:
        username = username.strip()
        if not username:
            return False, "Username cannot be empty."
        if self.user_exists(username):
            return False, "Username already exists."
        if len(password) < 6:
            return False, "Password must be at least 6 characters."
        self.users.append({"username": username, "password": self._hash_pw(password)})
        self._save()
        return True, "Registration successful."

    def authenticate(self, username: str, password: str) -> bool:
        hashed = self._hash_pw(password)
        return any(u["username"] == username and u["password"] == hashed for u in self.users)
