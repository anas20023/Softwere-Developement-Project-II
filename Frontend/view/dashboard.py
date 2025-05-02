import ttkbootstrap as tb
from ttkbootstrap.constants import *
import webbrowser
import requests
from tkinter import messagebox
from config.settings import API_VOTE_URL, API_CHECK_VOTE_URL
from utils.state import state

class DashboardFrame(tb.Frame):
    def __init__(self, master, suggestions, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.suggestions = suggestions
        self.style = tb.Style()
        self._configure_styles()
        self._build_ui()

    def _configure_styles(self):
        """Custom style configurations for modern look"""
        self.style.configure('modern.TLabelframe', 
                           bordercolor='#e0e0e0', 
                           lightcolor='#ffffff', 
                           darkcolor='#ffffff',
                           background='#ebebeb',
                           relief='flat',
                           borderwidth=2,
                           padding=(15, 10))
        
        self.style.configure('badge.TLabel', 
                           font=('Helvetica', 9, 'bold'),
                           padding=5,
                           foreground='#2d3436',
                           anchor='center'),
                        
        
        self.style.map('vote.TButton',
                      foreground=[('active', '!disabled', '#ffffff'), ('!active', '#ffffff')],
                      background=[('disabled', '#6c757d'), ('!disabled', '#4a90e2')])

    def _build_ui(self):
        # ─── Modern Scrollable Grid ─────────────────────────────────────────
        container = tb.Frame(self)
        container.pack(fill=BOTH, expand=YES, padx=15)

        canvas = tb.Canvas(container)
        vsb = tb.Scrollbar(container, orient="vertical", command=canvas.yview, bootstyle="primary")
        canvas.configure(yscrollcommand=vsb.set)
        
        vsb.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        
        grid_frame = tb.Frame(canvas,padding=(40, 10))
        canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        grid_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # ─── Modern Cards ───────────────────────────────────────────────────
        cols = 4
        for idx, sug in enumerate(self.suggestions):
            row, col = divmod(idx, cols)
            card = tb.Labelframe(
                grid_frame,
                text=f"{sug['course_code']} - {sug['course_name']}",
                style='modern.TLabelframe',
                padding=15,
            )

            # Header Section
            header = tb.Frame(card)
            header.pack(fill=X, pady=(0, 10))
            
            # Department Chip
            tb.Label(header, 
                    text=f"{sug['dept']}", 
                    bootstyle="secondary.inverse",
                    font=('Helvetica', 9, 'bold'),
                    padding=(5, 2)).pack(side=LEFT, padx=5)

            # Exam Type Badge
            exam_style = "success" if sug['exam_type'] == "Final" else "warning"
            tb.Label(header,
                    text=f"{sug['exam_type']}",
                    bootstyle=f"{exam_style}.inverse",
                    font=('Helvetica', 9),
                    padding=(8, 3)).pack(side=LEFT)

            # Votes Section
            votes_frame = tb.Frame(header)
            votes_frame.pack(side=RIGHT)
            
            votes_var = tb.StringVar(value=str(sug.get('stars', 0)))
            tb.Label(votes_frame, 
                    textvariable=votes_var,
                    bootstyle="warning",
                    font=('Helvetica', 12, 'bold'),
                    padding=(0, 0, 5, 0)).pack(side=LEFT)
            
            tb.Label(votes_frame, 
                    text="★",
                    bootstyle="warning",
                    font=('Helvetica', 14)).pack(side=LEFT)

            # Interactive Content
            content_frame = tb.Frame(card)
            content_frame.pack(fill=BOTH, expand=YES)

            # Description with improved typography
            tb.Label(content_frame,
                    text=sug['description'],
                    wraplength=350,
                    font=('Helvetica', 10),
                    bootstyle="secondary",
                    padding=(0, 5, 0, 15)).pack(anchor="w")

            # Action Bar
            action_bar = tb.Frame(card)
            action_bar.pack(fill=X, pady=(10, 0))
            
            # Attachment Button with icon
            att_btn = tb.Button(
                action_bar,
                text="📎 Open Attachment",
                bootstyle="link",
                command=lambda url=sug['attachment_url']: webbrowser.open(url)
            )
            att_btn.pack(side=LEFT)

            # Vote Button with modern styling
            vote_btn = tb.Button(
                action_bar,
                text="↑ Vote",
                style='vote.TButton',
                padding=(15, 5)
            )
            # Configure command AFTER button creation
            vote_btn.configure(
                command=lambda s=sug, v=votes_var, b=vote_btn: self._vote(s, v, b)
            )
            vote_btn.pack(side=RIGHT)
            self._check_vote(sug, vote_btn)

            card.grid(row=row, column=col, padx=10, pady=10, sticky=NSEW)

        # Configure columns to expand evenly
        for c in range(cols):
            grid_frame.columnconfigure(c, weight=1)

    def _check_vote(self, suggestion, btn):
        """Enable or disable vote button based on prior vote"""
        student_id = state.user_info.get('student_id')
        if not student_id:
            btn.state(['disabled'])
            return
        try:
            res = requests.post(API_CHECK_VOTE_URL, json={
                'student_id': student_id,
                'suggestion_id': suggestion['id']
            })
            if res.ok and res.json().get('voted'):
                btn.state(['disabled'])
            else:
                btn.state(['!disabled'])
        except:
            btn.state(['!disabled'])

    def _vote(self, suggestion, votes_var, btn):
        student_id = state.user_info.get('student_id')
        if not student_id:
            messagebox.showwarning("Login Required", "Please login to vote.")
            return
        try:
            res = requests.post(API_VOTE_URL, json={
                'student_id': student_id,
                'suggestion_id': suggestion['id']
            })
            res.raise_for_status()
            # Increment display
            new_count = int(votes_var.get()) + 1
            votes_var.set(str(new_count))
            btn.state(['disabled'])
        except Exception as e:
            messagebox.showerror("Vote Failed", f"Could not register vote:\n{e}")