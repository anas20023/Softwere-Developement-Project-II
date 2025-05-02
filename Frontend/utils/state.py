# Frontend/utils/state.py

class AppState:
    """
    Centralized state: track login status & user info.
    """
    def __init__(self):
        self.logged_in = False
        self.user_info = {}

    def login(self, info: dict):
        self.logged_in = True
        self.user_info = info

    def logout(self):
        self.logged_in = False
        self.user_info = {}

# single shared instance
state = AppState()
