from tkinter import messagebox, BOTH, YES, END
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from api import register_user, login_user
from session_manager import session
import requests

API_URL = "https://sgm.anasibnbelal.live/api/auth/suggetions/get"

class LoginApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera")
        self.title("Suggestion Sharing Platform - Login")
        self.geometry("1000x800")
        self.resizable(False, False)

        # Main container
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES)

        # Login frame
        self.frame = ttk.Frame(self.container, bootstyle="light", padding=20)
        self.frame.pack(pady=50, padx=50, fill=BOTH, expand=YES)

        # Header
        self.header_frame = ttk.Frame(self.frame, bootstyle="light")
        self.header_frame.pack(fill=X, pady=(0, 20))
        self.label = ttk.Label(
            self.header_frame,
            text="Login to Platform",
            font=("Inter", 24, "bold"),
            bootstyle="primary"
        )
        self.label.pack(pady=10)

        # Message label
        self.show_message = ttk.Label(
            self.frame,
            text="",
            font=("Inter", 12),
            bootstyle="secondary"
        )
        self.show_message.pack(pady=10, fill=X)

        # Input fields
        self.input_frame = ttk.Frame(self.frame, bootstyle="light")
        self.input_frame.pack(fill=X, pady=10)
        ttk.Label(self.input_frame, text="Student ID", font=("Inter", 12), bootstyle="secondary").pack(anchor="w", padx=10)
        self.student_id_entry = ttk.Entry(self.input_frame, bootstyle="primary", width=30, font=("Inter", 12))
        self.student_id_entry.insert(0, "Student ID")
        self.student_id_entry.pack(pady=5, ipady=5, fill=X)

        ttk.Label(self.input_frame, text="Password", font=("Inter", 12), bootstyle="secondary").pack(anchor="w", padx=10, pady=(10, 0))
        self.password_entry = ttk.Entry(self.input_frame, bootstyle="primary", width=30, show="*", font=("Inter", 12))
        self.password_entry.insert(0, "Password")
        self.password_entry.pack(pady=5, ipady=5, fill=X)

        # Buttons
        self.button_frame = ttk.Frame(self.frame, bootstyle="light")
        self.button_frame.pack(fill=X, pady=20)
        self.login_button = ttk.Button(self.button_frame, text="Login", bootstyle="success-outline", command=self.login, width=15)
        self.login_button.pack(pady=10, ipady=5)

        self.register_frame = ttk.Frame(self.frame, bootstyle="light")
        self.register_frame.pack(fill=X, pady=(10, 0))
        ttk.Label(self.register_frame, text="Don't have an Account?", font=("Inter", 12), bootstyle="secondary").pack(pady=6)
        self.register_button = ttk.Button(self.register_frame, text="Register", bootstyle="primary-outline", command=self.show_register, width=15)
        self.register_button.pack(pady=5, ipady=5)

        # Placeholder bindings
        self.student_id_entry.bind("<FocusIn>", self.clear_placeholder)
        self.password_entry.bind("<FocusIn>", self.clear_placeholder)
        self.student_id_entry.bind("<FocusOut>", self.reset_placeholder)
        self.password_entry.bind("<FocusOut>", self.reset_placeholder)

    def fetch_suggestions(self):
        try:
            resp = requests.get(API_URL)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch suggestions:\n{e}")
            return []

    def clear_placeholder(self, event):
        widget = event.widget
        if widget.get() in ["Student ID", "Password"]:
            widget.delete(0, END)
            if widget == self.password_entry:
                widget.config(show="*")

    def reset_placeholder(self, event):
        widget = event.widget
        if widget.get() == "":
            if widget == self.student_id_entry:
                widget.insert(0, "Student ID")
            elif widget == self.password_entry:
                widget.config(show="")
                widget.insert(0, "Password")

    def show_dashboard(self):
        self.after(1000, self.destroy)

    def login(self):
        sid = self.student_id_entry.get()
        pwd = self.password_entry.get()
        if sid in ("", "Student ID") or pwd in ("", "Password"):
            self.show_message.config(text="Enter your creds, fam", bootstyle="danger")
            return

        response = login_user(sid, pwd)
        if response.get("success"):
            messagebox.showinfo("Login Successful", "Welcome back!")
            session.login(user=response["student"], token=response["token"])
            self.show_message.config(text=f"Welcome back, {session.user['name']}!", bootstyle="success")
            self.show_dashboard()
        else:
            self.show_message.config(text=response.get("message", "Login failed"), bootstyle="danger")

    def show_register(self):
        RegisterApp(self)

class RegisterApp(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("1000x1000")
        self.resizable(False, False)
        self.title("Suggestion Sharing Platform - Register")

        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES)
        self.frame = ttk.Frame(self.container, bootstyle="light", padding=20)
        self.frame.pack(pady=30, padx=40, fill=BOTH, expand=YES)

        self.header_frame = ttk.Frame(self.frame, bootstyle="light")
        self.header_frame.pack(fill=X, pady=(0, 20))
        self.label = ttk.Label(self.header_frame, text="Create Account", font=("Inter", 24, "bold"), bootstyle="primary")
        self.label.pack(pady=10)

        self.show_message = ttk.Label(self.frame, text="", font=("Inter", 12), bootstyle="secondary")
        self.show_message.pack(pady=10, fill=X)

        self.entries = {}
        fields = [("Name", "name"), ("Student ID", "student_id"), ("Email", "email"),
                  ("Department", "dept"), ("Intake", "intake"), ("Section", "section"), ("Password", "password")]

        for placeholder, field in fields:
            field_frame = ttk.Frame(self.frame, bootstyle="light")
            field_frame.pack(fill=X, pady=5)
            ttk.Label(field_frame, text=placeholder, font=("Inter", 12), bootstyle="secondary").pack(anchor="w", padx=10)
            entry = ttk.Entry(field_frame, bootstyle="primary", width=30, font=("Inter", 12))
            entry.insert(0, placeholder)
            entry.pack(pady=5, ipady=5, fill=X)
            entry.bind("<FocusIn>", lambda e, w=entry: self.clear_placeholder(w))
            entry.bind("<FocusOut>", lambda e, w=entry, p=placeholder: self.reset_placeholder(w, p))
            if field == 'password':
                entry.config(show="*")
            self.entries[field] = entry

        self.register_button = ttk.Button(self.frame, text="Register", bootstyle="success-outline", command=self.register, width=15)
        self.register_button.pack(pady=20, ipady=5)

    def clear_placeholder(self, widget):
        if widget.get() in ["Name", "Student ID", "Email", "Department", "Intake", "Section", "Password"]:
            widget.delete(0, END)
            if widget == self.entries.get('password'):
                widget.config(show="*")

    def reset_placeholder(self, widget, placeholder):
        if widget.get() == "":
            widget.insert(0, placeholder)
            if placeholder == "Password":
                widget.config(show="")

    def register(self):
        data = {field: self.entries[field].get() for field in self.entries}
        if any(v in ["", *[p for p,_ in [("Name",""),("Student ID",""),("Email",""),("Department",""),("Intake",""),("Section",""),("Password","") ]]] for v in data.values()):
            self.show_message.config(text="All fields are required", bootstyle='danger')
            return
        response = register_user(data['name'], data['student_id'], data['email'], data['dept'], data['intake'], data['section'], data['password'])
        if response.get("success"):
            self.show_message.config(text=response["message"], bootstyle='success')
            self.after(3000, self.destroy)
        else:
            self.show_message.config(text=response.get("message", "Registration failed"), bootstyle='danger')

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()