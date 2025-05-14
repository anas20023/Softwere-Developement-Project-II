import customtkinter as ctk
import webbrowser
import requests
from app_state import AppState
from tkinter import messagebox

def open_url(url):
    webbrowser.open(url)

def render_card(parent, obj, app_state, refresh_callback, card_width=350):
    mode = ctk.get_appearance_mode()
    bg = "#1E293B" if mode.lower() == "dark" else "white"

    card = ctk.CTkFrame(
        parent,
        corner_radius=16,
        fg_color=bg,
        border_width=1,
        border_color="#334155" if mode.lower() == "dark" else "#E2E8F0",
        width=card_width,
        height=280
    )
    card.pack_propagate(False)

    # Top Section
    top_row = ctk.CTkFrame(card, fg_color="transparent")
    top_row.pack(fill="x", pady=(12, 6), padx=12)
    
    ctk.CTkLabel(
        top_row,
        text=obj["dept"],
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#94A3B8" if mode.lower() == "dark" else "#64748B"
    ).pack(side="left")

    vote_controls = ctk.CTkFrame(top_row, fg_color="transparent")
    vote_controls.pack(side="right")
    
    # Exam type badge
    ctk.CTkLabel(
        vote_controls,
        text=obj["exam_type"],
        font=ctk.CTkFont(size=10, weight="bold"),
        fg_color="#7A1CAC",
        text_color="white",
        corner_radius=2,
        padx=6,
        pady=3,
    ).pack(side="left", padx=(0, 6))

    # Star rating
    ctk.CTkLabel(
        vote_controls,
        text=f"{obj['stars']} ★",
        font=ctk.CTkFont(size=10),
        text_color="#FBBF24",
    ).pack(side="left", padx=(0, 6))

    # Vote button
    vote_btn = ctk.CTkButton(
        vote_controls,
        text="Vote",
        font=ctk.CTkFont(size=10, weight="bold"),
        fg_color="#F43F5E",
        hover_color="#E11D48",
        text_color="white",
        corner_radius=5,
        width=60,
        height=24,
    )

    if app_state.is_authenticated():
        student_id = app_state.get_user().get("student_Id")
        suggestion_id = obj["id"]
        has_voted = False

        try:
            response = requests.post(
                "https://sgm.anasibnbelal.live/api/auth/suggetions/checkVote",
                json={"student_id": student_id, "suggestion_id": suggestion_id}
            )
            if response.status_code == 200:
                #print(response.json())
                has_voted = response.json().get("voted")
                #print(has_voted)
        except Exception as e:
            messagebox.showerror("Error", f"Vote check failed: {str(e)}")

        vote_btn.configure(
            text="Voted" if has_voted else "Vote",
            fg_color="#10B981" if has_voted else "#F43F5E",
            hover_color="#059669" if has_voted else "#E11D48",
        )

        def handle_vote():
            try:
                if has_voted:
                    #message box
                    messagebox.showinfo("Info", "You have already voted.")
                    return
                else:
                    response = requests.post(
                        "https://sgm.anasibnbelal.live/api/auth/suggetions/giveVote",
                        json={"student_id": student_id, "suggestion_id": suggestion_id}
                    )
                
                if response.status_code in [200, 201]:
                    refresh_callback()
                else:
                    messagebox.showerror("Error", f"API Error: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Vote operation failed: {str(e)}")

        vote_btn.configure(command=handle_vote)
    else:
        vote_btn.configure(state="disabled")

    vote_btn.pack(side="left", padx=(0, 6))

    # Course Title
    ctk.CTkLabel(
        card,
        text=obj["course_name"],
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="#2563EB",
        text_color="white",
        corner_radius=1,
        padx=8,
        pady=10,
    ).pack(fill="x", padx=12, pady=(8, 12))

    # Course Code
    ctk.CTkLabel(
        card,
        text=obj["course_code"],
        font=ctk.CTkFont(size=12),
        text_color="#94A3B8" if mode.lower() == "dark" else "#64748B",
    ).pack(anchor="w", padx=12)

    # Description
    ctk.CTkLabel(
        card,
        text=obj["description"],
        font=ctk.CTkFont(size=12),
        text_color="#CBD5E1" if mode.lower() == "dark" else "#334155",
        wraplength=card_width - 24,
        justify="left",
    ).pack(fill="x", padx=12, pady=(6, 12))

    # Attachments Section
    ctk.CTkLabel(
        card,
        text="Attachments",
        font=ctk.CTkFont(size=12),
        text_color="#94A3B8" if mode.lower() == "dark" else "#475569",
    ).pack(anchor="w", padx=12, pady=(0, 6))

    # Attachment Row
    att_row = ctk.CTkFrame(card, fg_color="transparent")
    att_row.pack(fill="x", padx=12, pady=(0, 12))
    
    file_info = ctk.CTkFrame(att_row, fg_color="transparent")
    file_info.pack(side="left", fill="x", expand=True)
    
    ctk.CTkLabel(file_info, text="📎", font=ctk.CTkFont(size=14)).pack(side="left")
    fn = obj["course_name"]+ "." + obj["attachment_url"][-3:]
    ctk.CTkLabel(
        file_info,
        text=fn,
        font=ctk.CTkFont(size=12),
        text_color="#94A3B8" if mode.lower() == "dark" else "#64748B",
    ).pack(side="left", padx=(6, 0))

    download_btn = ctk.CTkButton(
        att_row,
        text="Download",
        font=ctk.CTkFont(size=10, weight="bold"),
        fg_color="#F43F5E",
        hover_color="#E11D48",
        text_color="white",
        corner_radius=5,
        command=lambda: open_url(obj["attachment_url"])
    )
    download_btn.pack(side="right",padx=(6, 0))

    # Footer
    footer = ctk.CTkFrame(card, fg_color="transparent")
    footer.pack(fill="x", pady=(0, 12), padx=12)
    
    ctk.CTkLabel(
        footer,
        text=f"Intake {obj['intake']}",
        font=ctk.CTkFont(size=10),
        text_color="#94A3B8" if mode.lower() == "dark" else "#64748B"
    ).pack(side="left")
    
    ctk.CTkLabel(
        footer,
        text="|",
        font=ctk.CTkFont(size=10),
        text_color="#64748B"
    ).pack(side="left", padx=6)
    
    ctk.CTkLabel(
        footer,
        text=f"Section {obj['section']}",
        font=ctk.CTkFont(size=10),
        text_color="#94A3B8" if mode.lower() == "dark" else "#64748B"
    ).pack(side="left")

    return card