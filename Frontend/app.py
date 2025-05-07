import ttkbootstrap as tb
from settings import APP_TITLE, WINDOW_SIZE, ICON_PATH, DEFAULT_THEME, DARK_THEME
from state import state
from dashboard import DashboardFrame
import requests
from tkinter import messagebox
from loginreg import LoginApp
API_URL = "https://sgm.anasibnbelal.live/api/auth/suggetions/get"

def fetch_suggestions():
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch suggestions:\n{e}")
        return []


def refresh_suggestions():
    global dash
    dash.destroy()
    suggestions = fetch_suggestions()
    dash = DashboardFrame(app, suggestions)
    dash.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=(50,10))

def on_login():
    LoginApp()
    print(state)
    

def on_profile():
    tb.messagebox.showinfo("Profile", "Profile feature is not implemented yet.")
    # Placeholder for profile functionality
    # You can implement the profile functionality her
    pass

if __name__ == '__main__':
    app = tb.Window(themename=DEFAULT_THEME)
    app.title(APP_TITLE)
    app.geometry(WINDOW_SIZE)
    app.resizable(False, False)
    app.iconbitmap(ICON_PATH)

    # grid weights
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure(2, weight=2)
    app.grid_rowconfigure(1, weight=1)
    # theme default
    app.style.theme_use("cosmo")
    # Create a style for the vote button

    # Row 0 buttons

    btn_refresh = tb.Button(app, text="Refresh", command=refresh_suggestions,
                            bootstyle="outline,success", padding=10)
    btn_refresh.grid(row=0, column=0, pady=10)

    # Conditionally show Login or Profile
    if getattr(state, 'user', None):
        btn_profile = tb.Button(app, text="Profile", command=on_profile,
                                bootstyle="outline,secondary", padding=10)
        btn_profile.grid(row=0, column=1, pady=10)
    else:
        btn_login = tb.Button(app, text="Login", command=on_login,
                              bootstyle="outline,primary", padding=10)
        btn_login.grid(row=0, column=1, pady=10)

    # Initial dashboard spanning all 3 columns
    suggestions = fetch_suggestions()
    dash = DashboardFrame(app, suggestions)
    dash.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=(50,10))

    app.mainloop()
