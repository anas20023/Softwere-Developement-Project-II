import ttkbootstrap as tb
from ttkbootstrap.constants import *
from session_manager import session
from loginreg import LoginApp
from dashboard import DashboardFrame
import requests
from tkinter import messagebox

API_URL = "https://sgm.anasibnbelal.live/api/auth/suggetions/get"

# Fetch suggestions helper
def fetch_suggestions():
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch suggestions:\n{e}")
        return []

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("Suggestion Sharing Platform")
        self.geometry("1200x800")
        self.resizable(False, False)

        # grid config
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top buttons frame
        self.btn_refresh = tb.Button(self, text="Refresh", command=self.refresh_suggestions,
                                     bootstyle="outline,success", padding=10)
        self.btn_refresh.grid(row=0, column=0, pady=10)

        # Placeholder for login/profile button
        self.btn_login = tb.Button(self, text="Login", command=self.open_login,
                                   bootstyle="outline,primary", padding=10)
        self.btn_profile = tb.Button(self, text="Profile", command=self.open_profile,
                                     bootstyle="outline,secondary", padding=10)
        self._place_auth_button()

        # Dashboard placeholder
        self.dash = None
        self.refresh_suggestions()

    def _place_auth_button(self):
        # remove both then place appropriate
        try:
            self.btn_login.grid_forget()
            self.btn_profile.grid_forget()
        except Exception:
            pass
        if session.is_logged_in:
            self.btn_profile.grid(row=0, column=1, pady=10)
        else:
            self.btn_login.grid(row=0, column=1, pady=10)

    def open_login(self):
        # open login window, pass callback
        LoginApp(on_success=self.on_login_success)

    def on_login_success(self):
        # called after successful login
        self._place_auth_button()

    def open_profile(self):
        # implement profile view
        messagebox.showinfo("Profile", f"Logged in as: {session.user['name']}")

    def refresh_suggestions(self):
        if self.dash:
            self.dash.destroy()
        suggestions = fetch_suggestions()
        self.dash = DashboardFrame(self, suggestions)
        self.dash.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=(50,10))

if __name__ == '__main__':
    app = App()
    app.mainloop()