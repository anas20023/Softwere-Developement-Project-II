import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from api import register_user, login_user

class LoginApp(ttk.Window):
    def __init__(self):
        super().__init__()
        
        self.title("Suggestion Sharing Platform || Login")
        self.geometry("800x600")
        self.resizable(False, False)

        # Configure styles
        self.style.configure('success.TLabel', background='#28a745', foreground='white', padding=10)
        self.style.configure('danger.TLabel', background='#dc3545', foreground='white', padding=10)
        self.style.configure('Large.TButton', font=('Inter semibold', 14), padding=(10, 5))
        self.style.configure('Tall.TEntry', padding=(10, 5))

        self.frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.frame.pack(pady=20, padx=10, fill="both", expand=True)

        self.label = ttk.Label(self.frame, text="Login", font=("Inter", 24))
        self.label.pack(pady=10)

        self.show_message = ttk.Label(self.frame, text="", font=("Arial", 14))
        self.show_message.pack(pady=10)

        self.student_id_entry = ttk.Entry(self.frame, style='Tall.TEntry', width=30, foreground='grey')
        self.student_id_entry = ttk.Entry(self.frame, style='Tall.TEntry', width=30)
        self.student_id_entry.insert(0, "Student ID")
        self.student_id_entry.pack(pady=5)

        self.password_entry = ttk.Entry(self.frame, style='Tall.TEntry', width=30, show="*")
        self.password_entry.insert(0, "Password")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.frame, text="Login", style='Large.TButton', 
                                    command=self.login)
        self.login_button.pack(pady=10)

        self.dont = ttk.Label(self.frame, text="Don't have an Account?", 
                            font=("Inter semibold", 14))
        self.dont.pack(pady=6)

        self.register_button = ttk.Button(self.frame, text="Register", style='Large.TButton',
                                       command=self.show_register)
        self.register_button.pack(pady=5)

        # Bind entry focus events
        self.student_id_entry.bind("<FocusIn>", self.clear_placeholder)
        self.password_entry.bind("<FocusIn>", self.clear_placeholder)

    def clear_placeholder(self, event):
        widget = event.widget
        if widget.get() in ["Student ID", "Password"]:
            widget.delete(0, END)
            if widget == self.password_entry:
                widget.config(show="*")

    def login(self):
        student_id = self.student_id_entry.get()
        password = self.password_entry.get()

        response = login_user(student_id, password)
        if response.get("success"):
            self.show_message.config(text=f"Welcome, {response['student']['name']}!", 
                                  style='success.TLabel')
        else:
            self.show_message.config(text=response.get("message", response.get('error', 'Unknown error')), 
                                  style='danger.TLabel')

    def show_register(self):
        RegisterApp(self)

class RegisterApp(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("500x600")
        self.resizable(False, False)
        self.title("Suggestion Sharing Platform || Register")

        # Configure styles
        self.style.configure('success.TLabel', background='#28a745', foreground='white', padding=10)
        self.style.configure('danger.TLabel', background='#dc3545', foreground='white', padding=10)
        self.style.configure('Tall.TEntry', padding=(10, 5))

        self.frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.frame.pack(pady=20, padx=10, fill="both", expand=True)

        self.label = ttk.Label(self.frame, text="Register", font=("Arial", 24))
        self.label.pack(pady=10)

        self.show_message = ttk.Label(self.frame, text="", font=("Arial", 14))
        self.show_message.pack(pady=10)

        self.entries = {}
        fields = [
            ("Name", "name"),
            ("Student ID", "student_id"),
            ("Department", "dept"),
            ("Intake", "intake"),
            ("Section", "section"),
            ("Password", "password")
        ]

        for placeholder, field in fields:
            entry = ttk.Entry(self.frame, style='Tall.TEntry', width=30)
            entry.insert(0, placeholder)
            entry.pack(pady=5)
            entry.bind("<FocusIn>", lambda e, w=entry: self.clear_placeholder(w))
            self.entries[field] = entry

        self.entries['password'].config(show="*")

        self.register_button = ttk.Button(self.frame, text="Register", style='Large.TButton',
                                       command=self.register)
        self.register_button.pack(pady=10)

    def clear_placeholder(self, widget):
        if widget.get() in ["Name", "Student ID", "Department", "Intake", "Section", "Password"]:
            widget.delete(0, END)
            if widget == self.entries['password']:
                widget.config(show="*")

    def register(self):
        data = {field: self.entries[field].get() for field in self.entries}
        
        if any(value in ["", "Name", "Student ID", "Department", "Intake", "Section", "Password"] 
               for value in data.values()):
            self.show_message.config(text="Fields can't be empty", style='danger.TLabel')
            return

        response = register_user(
            data['name'],
            data['student_id'],
            data['dept'],
            data['intake'],
            data['section'],
            data['password']
        )

        if response.get("success"):
            self.show_message.config(text=response["message"], style='success.TLabel')
            self.after(3000, self.destroy)
        else:
            self.show_message.config(text=response.get("message", "Registration failed"), 
                                   style='danger.TLabel')