import customtkinter as ctk
from tkinter import messagebox
import requests
import threading
from app_state import AppState
from auth_window import AuthWindow
from card import render_card
from profile_card import ProfileWindow
from upload import UploadWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Suggestion Sharing Platform")
        self.geometry("1200x700")
        self.app_state = AppState()

        # stash the raw data once fetched
        self.all_data = []
        # current filters
        self.filters = {
            "department": "",
            "course":     "",
            "intake":     "",
            "section":    "",
            "sort":       "",
            "examType":   ""
        }

        # --- TOP BUTTONS ---
        top = ctk.CTkFrame(self)
        top.pack(pady=20)
        self.btns = {}
        for txt, cmd in [
            ("Profile", self.open_profile),
            ("Upload Suggestion", self.open_upload),
            ("Refresh", self.fetch_data),
            ("Logout", self.logout),
            ("Login/Register", self.open_auth_window),
        ]:
            b = ctk.CTkButton(top, text=txt, command=cmd,
                              hover_color=("gray70","gray30"),
                              corner_radius=5)
            b.pack(side="left", padx=5,pady=15)
            self.btns[txt] = b
        ctk.CTkFrame(self, height=2).pack(padx=10, pady=5)
        self.update_top_buttons()

        # --- FILTER BAR ---
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(fill="x", pady=15)

        def mk_menu(name, label, width=150):
            m = ctk.CTkOptionMenu(
                self.filter_frame,
                values=[label],
                command=lambda v,n=name: self.on_filter_change(n, v),
                width=width,
                dynamic_resizing=False
            )
            m.set(label)
            return m

        self.menus = {
            "department": mk_menu("department", "All Departments"),
            "course":     mk_menu("course",     "All Courses"),
            "intake":     mk_menu("intake",     "All Intakes"),
            "section":    mk_menu("section",    "All Sections"),
            "sort":       mk_menu("sort",       "Sort By"),            # will override options below
            "examType":   mk_menu("examType",   "All Exam Types")
        }
        for m in self.menus.values():
            m.pack(side="left", padx=20, pady=5)

        # --- SCROLLABLE CARDS ---
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        self.scrollable.grid_columnconfigure((0,1,2), weight=1, uniform="col")

        # --- LOADING OVERLAY ---
        self.loading_overlay = ctk.CTkFrame(self, fg_color="gray20", corner_radius=5)
        self.loading_label   = ctk.CTkLabel(self.loading_overlay, text="Loading…",
                                            font=ctk.CTkFont(size=14, weight="bold"))
        self.loading_spinner = ctk.CTkProgressBar(self.loading_overlay,
                                                  mode="indeterminate", width=200, height=3)
        self.loading_label.pack(pady=(15,5))
        self.loading_spinner.pack(pady=(0,15))
        self.loading_overlay.place_forget()

        # first load
        self.fetch_data()

    def update_top_buttons(self):
        auth = self.app_state.is_authenticated()
        for b in self.btns.values():
            b.pack_forget()
        if auth:
            for t in ("Profile","Upload Suggestion","Refresh","Logout"):
                self.btns[t].pack(side="left", padx=5)
        else:
            self.btns["Login/Register"].pack(side="left", padx=5)

    def on_filter_change(self, name, value):
        self.filters[name] = "" if value.startswith("All") or value=="Sort By" else value
        self.apply_filters()

    def fetch_data(self):
        for w in self.scrollable.winfo_children():
            w.destroy()
        self.show_loading()
        threading.Thread(target=self._fetch_thread, daemon=True).start()

    def _fetch_thread(self):
        try:
            resp = requests.get("https://sgm.anasibnbelal.live/api/auth/suggetions/get")
            self.all_data = resp.json() or []
        except Exception as e:
            self.all_data = []
            self.after(0, lambda: messagebox.showerror("Error", f"Fetch failed: {e}"))
        finally:
            self.after(0, self.apply_filters)

    def apply_filters(self):
        data = self.all_data
        f = self.filters

        # build dynamic dropdown values just like your React hook
        depts    = sorted({s["dept"]         for s in data})
        courses  = sorted({s["course_code"]  for s in data
                           if (not f["department"] or s["dept"]==f["department"])})
        intakes  = sorted({s["intake"]       for s in data
                           if (not f["department"] or s["dept"]==f["department"])
                           and  (not f["course"]     or s["course_code"]==f["course"])})
        sections = sorted({s["section"]      for s in data
                           if (not f["department"] or s["dept"]==f["department"])
                           and  (not f["course"]     or s["course_code"]==f["course"])
                           and  (not f["intake"]     or s["intake"]==f["intake"])})
        exams    = sorted({s["exam_type"]    for s in data})

        # reconfigure each menu, keeping selection if still valid
        self._reconf("department", ["All Departments"] + depts,        f["department"])
        self._reconf("course",     ["All Courses"] + courses,         f["course"])
        self._reconf("intake",     ["All Intakes"] + intakes,         f["intake"])
        self._reconf("section",    ["All Sections"] + sections,       f["section"])
        # sort is static
        self._reconf("sort",       ["Sort By","Newest","Oldest","Most Stars"], f["sort"])
        self._reconf("examType",   ["All Exam Types"] + exams,         f["examType"])

        # now actually filter
        def keep(s):
            if f["department"] and s["dept"]            != f["department"]: return False
            if f["course"]     and s["course_code"]     != f["course"]:     return False
            if f["intake"]     and s["intake"]          != f["intake"]:     return False
            if f["section"]    and s["section"]         != f["section"]:    return False
            if f["examType"]   and s["exam_type"]       != f["examType"]:   return False
            return True

        filtered = [s for s in data if keep(s)]

        # then sort
        if f["sort"] == "Newest":
            filtered.sort(key=lambda s: s["created_at"], reverse=True)
        elif f["sort"] == "Oldest":
            filtered.sort(key=lambda s: s["created_at"])
        elif f["sort"] == "Most Stars":
            filtered.sort(key=lambda s: s.get("stars", 0), reverse=True)

        # render
        self.render_cards(filtered)
        self.hide_loading()

    def _reconf(self, key, options, current):
        menu = self.menus[key]
        menu.configure(values=options)
        label = ("All "+key.capitalize()) if key!="sort" else "Sort By"
        # restore if valid
        if current and current in options:
            menu.set(current)
        else:
            menu.set(label if key!="sort" else "Sort By")
            self.filters[key] = ""

    def render_cards(self, arr):
        for w in self.scrollable.winfo_children():
            w.destroy()
        per_row = 3
        rows = set()
        for idx, s in enumerate(arr):
            r, c = divmod(idx, per_row)
            if r not in rows:
                self.scrollable.grid_rowconfigure(r, minsize=224)
                rows.add(r)
            delay = idx * 80
            self.after(delay, lambda so=s, rr=r, cc=c: self.create_animated_card(so, rr, cc))

    def create_animated_card(self, obj, row, col):
        card = render_card(
            self.scrollable,
            obj,
            self.app_state,
            self.apply_filters,
            card_width=400
        )
        card.grid(row=row, column=col, padx=12, pady=40, sticky="nsew")
        def anim(i):
            p = max(12, 40 - 4*i)
            card.grid(pady=p)
            if i<7: self.after(20, anim, i+1)
        anim(0)

    def show_loading(self):
        self.loading_overlay.place(relx=0.5, rely=0.5, anchor="center")
        self.loading_spinner.start()
        self.loading_overlay.lift()

    def hide_loading(self):
        self.loading_spinner.stop()
        self.loading_overlay.place_forget()

    def open_auth_window(self):
        AuthWindow(self, lambda: [self.update_top_buttons(), self.apply_filters()])

    def logout(self):
        self.app_state.logout()
        messagebox.showinfo("Logged out", "You have been logged out")
        self.update_top_buttons()
        self.fetch_data()

    def open_profile(self):
        if self.app_state.is_authenticated():
            ProfileWindow(self, self.app_state)
        else:
            messagebox.showwarning("Profile", "Please login first")

    def open_upload(self):
        if self.app_state.is_authenticated():
            UploadWindow(self, self.app_state)
        else:
            messagebox.showwarning("Upload", "Please login first")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
