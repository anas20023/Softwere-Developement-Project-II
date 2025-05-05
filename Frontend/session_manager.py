# session_manager.py (same dir as app.py)
import json, os

class SessionManager:
    _instance = None
    SESSION_FILE = os.path.join(os.path.expanduser("~"), ".myapp_session.json")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.token = None
        self.user  = None
        self.is_logged_in = False
        self._load_from_disk()

    def _load_from_disk(self):
        if os.path.exists(self.SESSION_FILE):
            try:
                data = json.load(open(self.SESSION_FILE))
                self.token = data.get("token")
                self.user  = data.get("user")
                self.is_logged_in = bool(self.token)
            except Exception:
                pass

    def _save_to_disk(self):
        with open(self.SESSION_FILE, "w") as f:
            json.dump({"token": self.token, "user": self.user}, f)

    def login(self, user: dict, token: str):
        self.user = user
        self.token = token
        self.is_logged_in = True
        self._save_to_disk()

    def logout(self):
        self.user = None
        self.token = None
        self.is_logged_in = False
        try: os.remove(self.SESSION_FILE)
        except FileNotFoundError: pass

session = SessionManager()
