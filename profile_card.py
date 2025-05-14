# profile.py
import customtkinter as ctk
import requests
from tkinter import messagebox
import webbrowser

class ProfileWindow(ctk.CTkToplevel):
    def __init__(self, master, app_state):
        super().__init__(master)
        self.app_state = app_state
        self.title("User Profile")
        self.geometry("900x750")
        self._set_appearance_mode()
        self.attributes("-topmost", True)
        
        if not self.app_state.is_authenticated():
            self.destroy()
            return
        
        self.user_data = self.app_state.get_user()
        self._create_loading_screen()
        self.after(100, self._load_profile_data)

    def _set_appearance_mode(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def _create_loading_screen(self):
        self.loading_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.loading_frame.pack(expand=True, fill="both")
        
        ctk.CTkLabel(self.loading_frame, 
                    text="📊 Loading Profile...", 
                    font=("Arial", 18, "bold")).pack(pady=20)
        self.progress = ctk.CTkProgressBar(self.loading_frame, 
                                        mode="indeterminate",
                                        height=4,
                                        progress_color="#4B8BBE")
        self.progress.pack(pady=10, padx=50, fill="x")
        self.progress.start()

    def _load_profile_data(self):
        try:
            response = requests.get(
                f"https://sgm.anasibnbelal.live/api/auth/profile?id={self.user_data['student_Id']}"
            )
            self.data = response.json()
            self._destroy_loading_screen()
            self._create_main_interface()
        except Exception as e:
            self.destroy()
            messagebox.showerror("Error", f"Failed to load profile: {str(e)}")

    def _destroy_loading_screen(self):
        self.progress.stop()
        self.loading_frame.destroy()

    def _create_main_interface(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Profile Header Section
        self._create_profile_header(main_frame)
        
        # Details Section
        self._create_details_section(main_frame)
        
        # Total Stars Section
        self._create_total_stars_section(main_frame)
        
        # Suggestions Section
        self._create_suggestions_section(main_frame)

    def _create_profile_header(self, parent):
        header_frame = ctk.CTkFrame(parent, 
                                  height=100, 
                                  fg_color=("#2E86C1", "#1B4F72"),
                                  corner_radius=15)
        header_frame.pack(fill="x", pady=10)
        
        user = self.data['rows'][0]
        ctk.CTkLabel(header_frame,
                    text=f"{user['name']}",
                    font=("Arial", 24, "bold"),
                    text_color="white").pack(side="left", padx=30, pady=15)
        
        ctk.CTkLabel(header_frame,
                    text=f"🎓 {user['dept']} Department",
                    font=("Arial", 14),
                    text_color="white").pack(side="right", padx=30, pady=15)

    def _create_details_section(self, parent):
        details_frame = ctk.CTkFrame(parent, fg_color="transparent")
        details_frame.pack(fill="x", pady=10)
        
        user = self.data['rows'][0]
        details = [
            ("🆔 Student ID:", user['student_Id']),
            ("📧 Email:", user['email']),
            ("📅 Intake:", user['intake']),
            ("🏛️ Section:", user['section'])
        ]
        
        for label, value in details:
            row = ctk.CTkFrame(details_frame, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=20)
            
            ctk.CTkLabel(row, 
                         text=label,
                         font=("Arial", 14, "bold"),
                         width=150,
                         anchor="w").pack(side="left")
            
            ctk.CTkLabel(row, 
                         text=value,
                         font=("Arial", 14),
                         text_color=("#888888", "#CCCCCC")).pack(side="left")

    def _create_total_stars_section(self, parent):
        total_stars = sum(sug['stars'] for sug in self.data.get('sugs', []))
        
        stars_frame = ctk.CTkFrame(parent,
                                 fg_color=("#E3F2FD", "#2A3B4D"),
                                 corner_radius=10)
        stars_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(stars_frame,
                    text="⭐ Total Stars Earned",
                    font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=10)
        
        ctk.CTkLabel(stars_frame,
                    text=str(total_stars),
                    font=("Arial", 24, "bold"),
                    text_color="#FFD700").pack(side="right", padx=20, pady=10)

    def _create_suggestions_section(self, parent):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # Section Header
        ctk.CTkLabel(container, 
                     text="📝 Uploaded Suggestions",
                     font=("Arial", 16, "bold")).pack(anchor="w", pady=10)

        # Check for empty suggestions
        if not self.data.get('sugs'):
            self._create_empty_state(container)
            return

        # Scrollable Frame
        scroll_frame = ctk.CTkScrollableFrame(container, 
                                            height=300,
                                            fg_color=("#FFFFFF10", "#2A2A2A"))
        scroll_frame.pack(fill="both", expand=True)

        # Add suggestion cards
        for sug in self.data['sugs']:
            self._create_suggestion_card(scroll_frame, sug)

    def _create_empty_state(self, parent):
        empty_frame = ctk.CTkFrame(parent, fg_color="transparent")
        empty_frame.pack(fill="both", expand=True, pady=50)
        
        ctk.CTkLabel(empty_frame,
                    text="📭 No Suggestions Uploaded Yet",
                    font=("Arial", 14),
                    text_color=("#666666", "#999999")).pack()
        
        ctk.CTkLabel(empty_frame,
                    text="Start sharing your knowledge!",
                    font=("Arial", 12),
                    text_color=("#888888", "#AAAAAA")).pack(pady=5)

    def _create_suggestion_card(self, parent, sug):
        card = ctk.CTkFrame(parent,
                          border_width=1,
                          border_color=("#E0E0E0", "#404040"),
                          corner_radius=12)
        card.pack(fill="x", pady=5, padx=5)

        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=10)
        
        # Course Info
        course_frame = ctk.CTkFrame(header, fg_color="transparent")
        course_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(course_frame, 
                    text=sug['course_code'],
                    font=("Arial", 16, "bold")).pack(anchor="w")
        
        ctk.CTkLabel(course_frame,
                    text=f"{sug['course_name']} • {sug['exam_type']}",
                    font=("Arial", 12),
                    text_color=("#666666", "#999999")).pack(anchor="w")

        # Star Rating
        stars = sug['stars']
        st = f"{stars} ⭐" if stars > 0 else "No Stars"
        ctk.CTkLabel(header, 
                    text=st,
                    font=("Arial", 16),
                    text_color="#FFD700").pack(side="right")

        # Separator
        ctk.CTkFrame(card, 
                   height=1, 
                   fg_color=("#E0E0E0", "#404040")).pack(fill="x")

        # Description
        desc_frame = ctk.CTkFrame(card, fg_color="transparent")
        desc_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(desc_frame,
                    text=sug['description'],
                    font=("Arial", 12),
                    wraplength=700,
                    justify="left").pack(anchor="w")

        # Attachment
        if sug['attachment_url']:
            attach_frame = ctk.CTkFrame(card, fg_color="transparent")
            attach_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            ctk.CTkButton(attach_frame,
                         text="📎 Open Attachment",
                         font=("Arial", 12),
                         text_color=("#1E90FF", "#87CEFA"),
                         fg_color="transparent",
                         hover_color=("#F0F8FF", "#333333"),
                         command=lambda: webbrowser.open(sug['attachment_url']),
                         cursor="hand2").pack(side="left")