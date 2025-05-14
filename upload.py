import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import cloudinary
import cloudinary.uploader
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
API_KEY    = os.getenv('CLOUDINARY_API_KEY')
API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

if not all([CLOUD_NAME, API_KEY, API_SECRET]):
    raise RuntimeError("Missing Cloudinary config in environment!")

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET,
    secure=True
)

class UploadWindow(ctk.CTkToplevel):
    def __init__(self, master, app_state):
        super().__init__(master)
        self.title("Upload Suggestion")
        self.geometry("600x650")
        self.app_state = app_state
        self.api_endpoint = "https://sgm.anasibnbelal.live/api/auth/suggetions/create"
        self.max_file_size = 5 * 1024 * 1024  # 5 MB
        self.allowed_exts = ['.pdf', '.jpg', '.jpeg']

        # Force dark mode theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Main frame
        main_frame = ctk.CTkFrame(self, corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)

        # Fonts & spacing
        label_font = ("Poppins", 12)
        entry_font = ("Poppins", 11)
        spacer = 10

        # Header
        header = ctk.CTkLabel(main_frame, text="New Suggestion Submission", font=("Poppins", 18, "bold"))
        header.grid(row=0, column=0, pady=(0, spacer*2))

        # Course Info
        course_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        course_frame.grid(row=1, column=0, sticky="ew", pady=spacer)
        course_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(course_frame, text="Course Code:", font=label_font).grid(row=0, column=0, sticky="w", padx=5)
        self.course_code_var = ctk.StringVar()
        ctk.CTkEntry(course_frame, textvariable=self.course_code_var, font=entry_font, height=32, corner_radius=8).grid(row=0, column=1, sticky="ew", padx=5)

        ctk.CTkLabel(course_frame, text="Course Name:", font=label_font).grid(row=1, column=0, sticky="w", padx=5, pady=(spacer,0))
        self.course_name_var = ctk.StringVar()
        ctk.CTkEntry(course_frame, textvariable=self.course_name_var, font=entry_font, height=32, corner_radius=8).grid(row=1, column=1, sticky="ew", padx=5, pady=(spacer,0))

        ctk.CTkLabel(course_frame, text="Department:", font=label_font).grid(row=2, column=0, sticky="w", padx=5, pady=(spacer,0))
        self.dept_var = ctk.StringVar()
        ctk.CTkEntry(course_frame, textvariable=self.dept_var, font=entry_font, height=32, corner_radius=8).grid(row=2, column=1, sticky="ew", padx=5, pady=(spacer,0))

        # Exam Type & Description
        exam_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        exam_frame.grid(row=2, column=0, sticky="ew", pady=spacer)
        exam_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(exam_frame, text="Exam Type:", font=label_font).grid(row=0, column=0, sticky="w", padx=5)
        self.exam_type_var = ctk.StringVar(value="Final")
        ctk.CTkOptionMenu(exam_frame, values=["Midterm", "Final"], variable=self.exam_type_var, font=entry_font, corner_radius=8).grid(row=0, column=1, sticky="ew", padx=5)

        ctk.CTkLabel(exam_frame, text="Description:", font=label_font).grid(row=1, column=0, sticky="nw", padx=5, pady=(spacer,0))
        self.desc_text = ctk.CTkTextbox(exam_frame, font=entry_font, height=120, corner_radius=8)
        self.desc_text.grid(row=1, column=1, sticky="ew", padx=5, pady=(spacer,0))

        # File Upload
        file_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        file_frame.grid(row=3, column=0, sticky="ew", pady=spacer)
        file_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(file_frame, text="Attachment:", font=label_font).grid(row=0, column=0, sticky="w", padx=5)
        self.file_var = ctk.StringVar()
        file_label = ctk.CTkLabel(file_frame, textvariable=self.file_var, font=("Poppins", 10), anchor="w")
        file_label.grid(row=1, column=1, sticky="ew", padx=5, pady=(5,0))
        ctk.CTkButton(file_frame, text="Browse Files", command=self._choose_file, height=36, corner_radius=8).grid(row=0, column=1, sticky="e", padx=5)

        # Submit
        submit_btn = ctk.CTkButton(main_frame, text="Upload Suggestion", command=self._submit, height=42, corner_radius=10)
        submit_btn.grid(row=4, column=0, pady=(spacer*2, 0), sticky="ew", padx=50)

    def _choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("JPEG images", "*.jpg;*.jpeg")])
        if not file_path:
            return
        size = os.path.getsize(file_path)
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.allowed_exts:
            messagebox.showerror("Invalid File", "Only PDF or JPEG files up to 5MB are allowed.")
            return
        if size > self.max_file_size:
            messagebox.showerror("File Too Large", "File must be 5MB or smaller.")
            return
        self.file_var.set(os.path.basename(file_path))
        self.selected_file = file_path

    def _submit(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showwarning("No File", "Please select a file to upload.")
            return
        try:
            resp = cloudinary.uploader.upload(self.selected_file, resource_type="auto")
            url = resp.get('secure_url')
        except Exception as e:
            messagebox.showerror("Upload Failed", f"Cloud upload failed: {e}")
            return
        payload = {
            "uploaded_by": self.app_state.get_user().get("student_Id"),
            "course_code": self.course_code_var.get(),
            "course_name": self.course_name_var.get(),
            "dept": self.dept_var.get(),
            "intake": self.app_state.get_user().get("intake"),
            "section": self.app_state.get_user().get("section"),
            "exam_type": self.exam_type_var.get(),
            "description": self.desc_text.get("0.0", "end").strip(),
            "attachment_url": url
        }
        try:
            res = requests.post(self.api_endpoint, json=payload)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Submission Failed", f"Server error: {e}")
            return
        messagebox.showinfo("Success", "Suggestion uploaded successfully.")
        self.destroy()