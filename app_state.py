import json
import os

class AppState:
    _instance = None
    _session_file = os.path.join(os.path.expanduser("~"), ".sgm_session.json")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance.logged_in = False
            cls._instance.user_data = {}
            cls._instance._load_state()
        return cls._instance

    def _load_state(self):
        try:
            if os.path.exists(self._session_file):
                with open(self._session_file, "r") as f:
                    data = json.load(f)
                    self.logged_in = data.get("logged_in", False)
                    self.user_data = data.get("user_data", {})
        except Exception:
            self.logged_in = False
            self.user_data = {}

    def _save_state(self):
        try:
            data = {
                "logged_in": self.logged_in,
                "user_data": self.user_data
            }
            with open(self._session_file, "w") as f:
                json.dump(data, f)
        except Exception:
            pass

    def login(self, user_data):
        self.logged_in = True
        self.user_data = user_data
        self._save_state()

    def logout(self):
        self.logged_in = False
        self.user_data = {}
        try:
            if os.path.exists(self._session_file):
                os.remove(self._session_file)
        except Exception:
            pass

    def is_authenticated(self):
        return self.logged_in

    def get_user(self):
        return self.user_data