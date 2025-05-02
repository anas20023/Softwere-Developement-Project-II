import ttkbootstrap as tb
from ttkbootstrap.constants import TOP
from config.settings import APP_TITLE, WINDOW_SIZE, ICON_PATH, DEFAULT_THEME, DARK_THEME
from utils.state import state
from view.dashboard import DashboardFrame
import requests
from tkinter import messagebox

API_URL = "https://sgm.anasibnbelal.live/api/auth/suggetions/get"


def fetch_suggestions():
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch suggestions:\n{e}")
        return []


def toggle_theme():
    current = app.style.theme.name
    new = DARK_THEME if current == DEFAULT_THEME else DEFAULT_THEME
    app.style.theme_use(new)
def refresh_suggestions():
    global dash
    dash.destroy()
    suggestions = fetch_suggestions()
    dash = DashboardFrame(app, suggestions)
    dash.pack(fill="both", expand=True, padx=10, pady=(50,10))

if __name__ == '__main__':
    app = tb.Window(themename=DEFAULT_THEME)
    app.title(APP_TITLE)
    app.geometry(WINDOW_SIZE)
    app.resizable(False, False)
    app.iconbitmap(ICON_PATH)

    # Theme toggle
    btn = tb.Button(app, text="Toggle Theme", command=toggle_theme, bootstyle="info,outline", padding=10)
    btn.pack(side=TOP, anchor='w', padx=10, pady=10)
    btn = tb.Button(app, text="Refresh", command=refresh_suggestions, bootstyle="success,outline", padding=10)
    btn.pack(side=TOP, anchor='center', padx=10, pady=10)

    # Fetch real suggestions
    suggestions = fetch_suggestions()

    # Dashboard view
    dash = DashboardFrame(app, suggestions)
    dash.pack(fill="both", expand=True, padx=10, pady=(50,10))

    app.mainloop()
