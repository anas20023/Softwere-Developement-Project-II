import customtkinter as ctk
import requests
import threading
from tkinter import messagebox
from app_state import AppState

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AuthWindow(ctk.CTkToplevel):
    def __init__(self, master, refresh_callback):
        super().__init__(master)
        self.attributes("-topmost", True)
        self.title("Suggestion Sharing Platform || Login/Register")
        self.geometry("900x700")
        self.refresh_callback = refresh_callback
        self.app_state = AppState()

        # Configure main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Mode selector
        self.mode_var = ctk.StringVar(value="Login")
        self.mode_selector = ctk.CTkSegmentedButton(
            self, 
            values=["Login", "Register"],
            variable=self.mode_var,
            command=self.switch_form,
            height=50,
            width=600,
            selected_color="#1F6AA5",
            selected_hover_color="#144870",
            unselected_color="#2F2F2F",
            unselected_hover_color="#404040",
            font=("Poppins", 14)
        )
        self.mode_selector.grid(row=0, column=0, pady=40)

        # Form container
        self.form_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#2B2B2B")
        self.form_frame.grid(row=1, column=0, padx=80, pady=(10, 40), sticky="nsew")
        self.form_frame.grid_columnconfigure(1, weight=1)
        
        self.create_login_form()

    def switch_form(self, value):
        # Clear current form
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        # Create new form based on selection
        if value == "Login":
            self.create_login_form()
        else:
            self.create_register_form()

    def create_login_form(self):
        self.form_frame.grid_columnconfigure(1, weight=1, minsize=300)
        
        form_elements = [
            ("Student ID", "text", "🎒 Enter Student ID"),
            ("Password", "password", "🔑 Enter Password")
        ]

        for row, (label, entry_type, placeholder) in enumerate(form_elements):
            ctk.CTkLabel(self.form_frame, 
                        text=label,
                        font=("Poppins", 14),
                        anchor="w").grid(row=row, column=0, padx=(40, 20), pady=10, sticky="e")
            
            entry = ctk.CTkEntry(
                self.form_frame,
                placeholder_text=placeholder,
                width=200,
                height=50,
                corner_radius=10,
                border_width=2,
                fg_color="#1E1E1E",
                border_color="#3E3E3E",
                font=("Poppins", 14)
            )
            if entry_type == "password":
                entry.configure(show="•")
            entry.grid(row=row, column=1, padx=(0, 40), pady=10, sticky="ew")
            
            if label == "Student ID":
                self.student_id_entry = entry
            else:
                self.password_entry = entry

        self.login_btn = ctk.CTkButton(
            self.form_frame,
            text="Sign In →",
            command=self.login_user,
            height=40,
            width=200,
            corner_radius=10,
            fg_color="#1F6AA5",
            hover_color="#144870",
            font=("Poppins", 14)
        )
        self.login_btn.grid(row=len(form_elements)+1, column=0, columnspan=2, pady=40)

        self.loading_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=("Poppins", 14)
        )
        self.loading_label.grid(row=len(form_elements)+2, column=0, columnspan=2)
        self.loading_label.grid_remove()

    def create_register_form(self):
        self.form_frame.grid_columnconfigure(1, weight=1, minsize=300)
        
        form_fields = [
            ("👤 Name", "text", "Enter Full Name"),
            ("🎒 Student ID", "text", "Enter Student ID"),
            ("🏛 Department", "text", "Enter Department"),
            ("📅 Intake", "number", "e.g., 50"),
            ("🔢 Section", "number", "e.g., 1"),
            ("📧 Email", "email", "example@domain.com"),
            ("🔑 Password", "password", "Enter Password")
        ]

        for row, (label, field_type, placeholder) in enumerate(form_fields):
            ctk.CTkLabel(self.form_frame,
                       text=label,
                       font=("Poppins", 14),
                       anchor="w").grid(row=row, column=0, padx=(40, 20), pady=10, sticky="e")
            
            entry = ctk.CTkEntry(
                self.form_frame,
                placeholder_text=placeholder,
                width=200,
                height=40,
                corner_radius=10,
                border_width=2,
                fg_color="#1E1E1E",
                border_color="#3E3E3E",
                font=("Poppins", 14)
            )
            
            if field_type == "password":
                entry.configure(show="•")
            entry.grid(row=row, column=1, padx=(0, 40), pady=10, sticky="ew")
            
            if "Name" in label: self.name_entry = entry
            elif "Student ID" in label: self.student_id_entry = entry
            elif "Department" in label: self.dept_entry = entry
            elif "Intake" in label: self.intake_entry = entry
            elif "Section" in label: self.section_entry = entry
            elif "Email" in label: self.email_entry = entry
            else: self.password_entry = entry

        self.register_btn = ctk.CTkButton(
            self.form_frame,
            text="Create Account →",
            command=self.register_user,
            height=55,
            width=100,
            corner_radius=10,
            fg_color="#1F6AA5",
            hover_color="#144870",
            font=("Poppins", 14)
        )
        self.register_btn.grid(row=len(form_fields)+1, column=0, columnspan=2, pady=30)

        self.register_loading = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=("Poppins", 14)
        )
        self.register_loading.grid(row=len(form_fields)+2, column=0, columnspan=2)
        self.register_loading.grid_remove()

    def login_user(self):
        student_id = self.student_id_entry.get()
        password = self.password_entry.get()
        if not student_id or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        self.login_btn.configure(state="disabled", text="Logging in...")
        self.loading_label.configure(text="Processing...")
        self.loading_label.grid()

        threading.Thread(target=self.perform_login, args=(student_id, password), daemon=True).start()

    def perform_login(self, student_id, password):
        payload = {"studentId": student_id, "password": password}
        try:
            response = requests.post(
                "https://sgm.anasibnbelal.live/api/auth/login", json=payload
            )
            self.after(0, self.handle_login_response, response)
        except Exception as e:
            self.after(0, self.handle_login_error, e)

    def handle_login_response(self, response):
        self.loading_label.grid_remove()
        self.login_btn.configure(state="normal", text="Sign In →")
        if response.status_code == 200:
            data = response.json()
            self.app_state.login(data["student"])
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", response.json().get("msg", "Login failed"))

    def handle_login_error(self, error):
        self.loading_label.grid_remove()
        self.login_btn.configure(state="normal", text="Sign In →")
        messagebox.showerror("Error", str(error))

    def register_user(self):
        payload = {
            "name": self.name_entry.get(),
            "student_Id": self.student_id_entry.get(),
            "dept": self.dept_entry.get(),
            "intake": self.intake_entry.get(),
            "section": self.section_entry.get(),
            "password": self.password_entry.get(),
            "email": self.email_entry.get(),
        }
        try:
            intake = int(payload["intake"])
            section = int(payload["section"])
        except:
            messagebox.showerror("Error", "Intake and Section must be numbers")
            return

        if not all(payload.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        self.register_btn.configure(state="disabled", text="Registering...")
        self.register_loading.configure(text="Processing...")
        self.register_loading.grid()

        threading.Thread(target=self.perform_register, args=(payload,), daemon=True).start()

    def perform_register(self, payload):
        try:
            response = requests.post(
                "https://sgm.anasibnbelal.live/api/auth/register", json=payload
            )
            self.after(0, self.handle_register_response, response)
        except Exception as e:
            self.after(0, self.handle_register_error, e)

    def handle_register_response(self, response):
        self.register_loading.grid_remove()
        self.register_btn.configure(state="normal", text="Create Account →")
        if response.status_code == 201:
            messagebox.showinfo("Success", "Registered successfully. Please login.")
            self.mode_var.set("Login")
            self.switch_form("Login")
        else:
            messagebox.showerror("Error", response.json().get("msg", "Registration failed"))

    def handle_register_error(self, error):
        self.register_loading.grid_remove()
        self.register_btn.configure(state="normal", text="Create Account →")
        messagebox.showerror("Error", str(error))