import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from api import register_user, login_user

class LoginApp(ttk.Window):
    def __init__(self):
        # Initialize with a specific theme
        super().__init__(themename="litera")
        
        self.title("Suggestion Sharing Platform - Login")
        self.geometry("1000x800")
        self.resizable(False, False)

        # Create a container with gradient background
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES)
        
        # Create card-like frame for login
        self.frame = ttk.Frame(self.container, bootstyle="light", padding=20)
        self.frame.pack(pady=50, padx=50, fill=BOTH, expand=YES)

        # Add header with logo styling
        self.header_frame = ttk.Frame(self.frame, bootstyle="light")
        self.header_frame.pack(fill=X, pady=(0, 20))
        
        self.label = ttk.Label(
            self.header_frame, 
            text="Login to Platform", 
            font=("Inter", 24, "bold"),
            bootstyle="primary"
        )
        self.label.pack(pady=10)

        # Message display with better styling
        self.show_message = ttk.Label(
            self.frame, 
            text="", 
            font=("Inter", 12),
            bootstyle="secondary"
        )
        self.show_message.pack(pady=10, fill=X)
        
        # Input fields with better styling
        self.input_frame = ttk.Frame(self.frame, bootstyle="light")
        self.input_frame.pack(fill=X, pady=10)
        
        # Student ID field
        ttk.Label(
            self.input_frame, 
            text="Student ID", 
            font=("Inter", 12),
            bootstyle="secondary"
        ).pack(anchor="w", padx=10)
        
        self.student_id_entry = ttk.Entry(
            self.input_frame, 
            bootstyle="primary", 
            width=30,
            font=("Inter", 12)
        )
        self.student_id_entry.insert(0, "Student ID")
        self.student_id_entry.pack(pady=5, ipady=5, fill=X)

        # Password field
        ttk.Label(
            self.input_frame, 
            text="Password", 
            font=("Inter", 12),
            bootstyle="secondary"
        ).pack(anchor="w", padx=10, pady=(10, 0))
        
        self.password_entry = ttk.Entry(
            self.input_frame, 
            bootstyle="primary", 
            width=30, 
            show="*",
            font=("Inter", 12)
        )
        self.password_entry.insert(0, "Password")
        self.password_entry.pack(pady=5, ipady=5, fill=X)

        # Button area
        self.button_frame = ttk.Frame(self.frame, bootstyle="light")
        self.button_frame.pack(fill=X, pady=20)
        
        self.login_button = ttk.Button(
            self.button_frame, 
            text="Login", 
            bootstyle="success-outline", 
            command=self.login,
            width=15
        )
        self.login_button.pack(pady=10, ipady=5)

        # Registration section
        self.register_frame = ttk.Frame(self.frame, bootstyle="light")
        self.register_frame.pack(fill=X, pady=(10, 0))
        
        self.dont = ttk.Label(
            self.register_frame, 
            text="Don't have an Account?", 
            font=("Inter", 12),
            bootstyle="secondary"
        )
        self.dont.pack(pady=6)

        self.register_button = ttk.Button(
            self.register_frame, 
            text="Register", 
            bootstyle="primary-outline", 
            command=self.show_register,
            width=15
        )
        self.register_button.pack(pady=5, ipady=5)

        # Bind entry focus events
        self.student_id_entry.bind("<FocusIn>", self.clear_placeholder)
        self.password_entry.bind("<FocusIn>", self.clear_placeholder)
        self.student_id_entry.bind("<FocusOut>", self.reset_placeholder)
        self.password_entry.bind("<FocusOut>", self.reset_placeholder)

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

    def login(self):
        student_id = self.student_id_entry.get()
        password = self.password_entry.get()
        
        # Validate inputs aren't placeholders
        if student_id == "Student ID" or password == "Password":
            self.show_message.config(text="Please enter your credentials", bootstyle="danger")
            return

        response = login_user(student_id, password)
        if response.get("success"):
            self.show_message.config(text=f"Welcome, {response['student']['name']}!", bootstyle='success')
        else:
            self.show_message.config(text=response.get("message", response.get('error', 'Unknown error')), bootstyle='danger')

    def show_register(self):
        RegisterApp(self)

class RegisterApp(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("1000x1000")
        self.resizable(False, False)
        self.title("Suggestion Sharing Platform - Register")

        # Main container
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES)
        
        # Card-like frame
        self.frame = ttk.Frame(self.container, bootstyle="light", padding=20)
        self.frame.pack(pady=40, padx=40, fill=BOTH, expand=YES)

        # Header
        self.header_frame = ttk.Frame(self.frame, bootstyle="light")
        self.header_frame.pack(fill=X, pady=(0, 20))
        
        self.label = ttk.Label(
            self.header_frame, 
            text="Create Account", 
            font=("Inter", 24, "bold"),
            bootstyle="primary"
        )
        self.label.pack(pady=10)

        # Message display
        self.show_message = ttk.Label(
            self.frame, 
            text="", 
            font=("Inter", 12),
            bootstyle="secondary"
        )
        self.show_message.pack(pady=10, fill=X)

        # Form fields
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
            field_frame = ttk.Frame(self.frame, bootstyle="light")
            field_frame.pack(fill=X, pady=5)
            
            ttk.Label(
                field_frame, 
                text=placeholder, 
                font=("Inter", 12),
                bootstyle="secondary"
            ).pack(anchor="w", padx=10)
            
            entry = ttk.Entry(
                field_frame, 
                bootstyle="primary", 
                width=30,
                font=("Inter", 12)
            )
            entry.insert(0, placeholder)
            entry.pack(pady=5, ipady=5, fill=X)
            
            entry.bind("<FocusIn>", lambda e, w=entry: self.clear_placeholder(w))
            entry.bind("<FocusOut>", lambda e, w=entry, p=placeholder: self.reset_placeholder(w, p))
            self.entries[field] = entry

            if field == 'password':
                self.entries['password'].config(show="*")

        # Button area
        self.button_frame = ttk.Frame(self.frame, bootstyle="light")
        self.button_frame.pack(fill=X, pady=20)
        
        self.register_button = ttk.Button(
            self.button_frame, 
            text="Register", 
            bootstyle="success-outline", 
            command=self.register,
            width=15
        )
        self.register_button.pack(pady=10, ipady=5)

    def clear_placeholder(self, widget):
        if widget.get() in ["Name", "Student ID", "Department", "Intake", "Section", "Password"]:
            widget.delete(0, END)
            if widget == self.entries['password']:
                widget.config(show="*")

    def reset_placeholder(self, widget, placeholder):
        if widget.get() == "":
            widget.insert(0, placeholder)
            if placeholder == "Password":
                widget.config(show="")

    def register(self):
        data = {field: self.entries[field].get() for field in self.entries}
        
        if any(value in ["", "Name", "Student ID", "Department", "Intake", "Section", "Password"] for value in data.values()):
            self.show_message.config(text="All fields are required", bootstyle='danger')
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
            self.show_message.config(text=response["message"], bootstyle='success')
            # Show success message for 3 seconds then close
            self.after(3000, self.destroy)
        else:
            self.show_message.config(text=response.get("message", "Registration failed"), bootstyle='danger')

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()